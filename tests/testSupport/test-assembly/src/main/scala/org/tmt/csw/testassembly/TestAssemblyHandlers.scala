package org.tmt.csw.testassembly

import java.io.{File, FileOutputStream}
import org.apache.pekko.actor.typed.{ActorSystem, Behavior}
import org.apache.pekko.actor.typed.scaladsl.{ActorContext, Behaviors}
import csw.command.client.messages.TopLevelActorMessage
import csw.framework.models.CswContext
import csw.framework.scaladsl.ComponentHandlers
import csw.location.api.models.{ComponentId, ComponentType, Location, LocationRemoved, LocationUpdated, TrackingEvent}
import csw.logging.api.scaladsl.Logger
import csw.params.commands.CommandResponse._
import csw.params.commands.{CommandName, ControlCommand, Observe, Setup}
import csw.time.core.models.{TAITime, UTCTime}
import csw.params.core.models.{Angle, Coords, Id, ProperMotion}
import csw.params.events.{Event, EventKey, EventName, SystemEvent}

import scala.concurrent.{Await, ExecutionContextExecutor}
import TestAssemblyHandlers._
import org.apache.pekko.util.Timeout
import csw.command.client.CommandServiceFactory
import csw.location.api.models.Connection.HttpConnection
import csw.params.core.generics.KeyType
import csw.params.core.generics.KeyType.{CoordKey, TAITimeKey, UTCTimeKey}
import csw.params.core.models.Coords.EqFrame.FK5
import csw.params.core.models.Coords.SolarSystemObject.Venus
import csw.prefix.models.Prefix
import csw.prefix.models.Subsystem.CSW

import java.time.Instant
import scala.concurrent.duration._

object TestAssemblyHandlers {

  // Event published by python code and subscribed to here
  private val prefix = Prefix(CSW, "TestPublisher")
  private val eventNames = List(
    "testEvent1",
    "testEvent2",
    "testEvent3",
    "testEvent4"
  ).map(EventName.apply).toSet
  private val eventKeys = eventNames.map(EventKey(prefix, _))

  // Generate a test file with the JSON for the received events, as an easy way to compare with the expected values
  private val eventTestFile = new File("/tmp/PyTestAssemblyEventHandlers.out")

  // Generate a test file with the JSON for the received command responses, as an easy way to compare with the expected values
  private val commandTestFile = new File("/tmp/PyTestAssemblyCommandResponses.out")

  // Actor to receive events
  private def eventHandler(log: Logger): Behavior[Event] = {
    def handleEvent(event: SystemEvent): Unit = {
      log.info(s"Received event: $event")
      // sort params for comparison
      val params = event.paramSet.toList.sortBy(_.keyName).mkString(", ")
      val s      = s"SystemEvent(${event.eventName.name}, $params)\n"
      // Create the file when the first event is received from the test, close it on the last
      val append = event.eventName.name != "testEvent1"
      val testFd = new FileOutputStream(eventTestFile, append)
      testFd.write(s.getBytes)
      log.info(s"XXX Writing to $eventTestFile")
      testFd.close()
    }

    Behaviors.receive { (_, msg) =>
      msg match {
        case event: SystemEvent =>
          log.info(s"received event: $event")
          try {
            handleEvent(event)
          }
          catch {
            case ex: Exception =>
              log.error(s"Test failed for event $event", ex = ex)
          }
          Behaviors.same
        case x =>
          log.error(s"Unexpected message: $x")
          Behaviors.same
      }
    }
  }
}

/**
 * Domain specific logic should be written in below handlers.
 * This handlers gets invoked when component receives messages/commands from other component/entity.
 * For example, if one component sends Submit(Setup(args)) command to TestHcd,
 * This will be first validated in the supervisor and then forwarded to Component TLA which first invokes validateCommand hook
 * and if validation is successful, then onSubmit hook gets invoked.
 * You can find more information on this here : https://tmtsoftware.github.io/csw/commons/framework.html
 */
class TestAssemblyHandlers(ctx: ActorContext[TopLevelActorMessage], cswCtx: CswContext) extends ComponentHandlers(ctx, cswCtx) {

  import cswCtx._

  implicit val system: ActorSystem[Nothing] = ctx.system
  implicit val ec: ExecutionContextExecutor = ctx.executionContext

  implicit def timeout: Timeout = new Timeout(20.seconds)

  private val log = loggerFactory.getLogger

  // See tests/test_commands_with_assembly.py
  private val pythonConnection = HttpConnection(ComponentId(Prefix(CSW, "pycswTest"), ComponentType.Service))

  log.info("Initializing test assembly...")
  startSubscribingToEvents()

  override def initialize(): Unit = {}

  private def startSubscribingToEvents(): Unit = {
    val eventHandlerActor = ctx.spawn(eventHandler(log), "eventHandlerActor")
    eventService.defaultSubscriber
      .subscribeActorRef(eventKeys, eventHandlerActor)
  }

  override def onLocationTrackingEvent(trackingEvent: TrackingEvent): Unit = {
    trackingEvent match {
      case LocationUpdated(location) if location.connection == pythonConnection =>
        sendCommandsToPython(location)
      case LocationRemoved(connection) if connection == pythonConnection =>
        log.info(s"XXX python based service was removed from Location Service")
      case _ =>
    }
  }

  override def validateCommand(runId: Id, controlCommand: ControlCommand): ValidateCommandResponse = Accepted(runId)

  override def onSubmit(runId: Id, controlCommand: ControlCommand): SubmitResponse = {
    controlCommand match {
      case obs: Observe => onObserve(runId, obs)
      case setup: Setup => onSetup(runId, setup)
    }
  }

  // noinspection ScalaUnusedSymbol
  private def onObserve(runId: Id, observe: Observe): SubmitResponse = {
    Error(runId, "Observe not handled")
  }

  private def onSetup(runId: Id, setup: Setup): SubmitResponse = {
    if (setup.commandName.name == "longRunningCommand") {
      cswCtx.timeServiceScheduler.scheduleOnce(UTCTime.after(1.seconds))(
        cswCtx.commandResponseManager.updateCommand(Completed(runId))
      )
      Started(runId)
    }
    else Completed(runId)
  }

  override def onOneway(runId: Id, controlCommand: ControlCommand): Unit = {}

  override def onShutdown(): Unit = {}

  override def onGoOffline(): Unit = {}

  override def onGoOnline(): Unit = {}

  override def onDiagnosticMode(startTime: UTCTime, hint: String): Unit = {}

  override def onOperationsMode(): Unit = {}

  // Dummy test command
  private def makeTestCommand(commandName: String): ControlCommand = {
    import Angle._
    import Coords._

    val basePosKey = CoordKey.make("BasePosition")
    val cmdKey     = KeyType.FloatKey.make("cmdValue")
    val utcTimeKey = UTCTimeKey.make("utcTimeValue")
    val taiTimeKey = TAITimeKey.make("taiTimeValue")

    val pm = ProperMotion(0.5, 2.33)
    val eqCoord = EqCoord(
      ra = "12:13:14.15",
      dec = "-30:31:32.3",
      frame = FK5,
      pmx = pm.pmx,
      pmy = pm.pmy
    )
    val solarSystemCoord = SolarSystemCoord(Tag("BASE"), Venus)
    val minorPlanetCoord = MinorPlanetCoord(
      Tag("GUIDER1"),
      2000,
      90.degree,
      2.degree,
      100.degree,
      1.4,
      0.234,
      220.degree
    )
    val cometCoord = CometCoord(
      Tag("BASE"),
      2000.0,
      90.degree,
      2.degree,
      100.degree,
      1.4,
      0.234
    )
    val altAzCoord = AltAzCoord(Tag("BASE"), 301.degree, 42.5.degree)
    val posParam = basePosKey.set(
      eqCoord,
      solarSystemCoord,
      minorPlanetCoord,
      cometCoord,
      altAzCoord
    )
    //    val timeParam =

    Setup(componentInfo.prefix, CommandName(commandName), None)
      .add(posParam)
      .add(cmdKey.set(1.0f, 2.0f, 3.0f))
      .add(utcTimeKey.set(UTCTime(Instant.parse("2021-09-17T09:17:08.608242344Z"))))
      .add(taiTimeKey.set(TAITime(Instant.parse("2021-09-17T09:17:45.610701219Z"))))
  }

  // Send some test commands to the python based command service
  // See tests/test_commands_with_assembly.py.
  private def sendCommandsToPython(location: Location): Unit = {
    log.info(s"XXX python based service is located: $location")
    val pythonService = CommandServiceFactory.make(location)

    val testFd = new FileOutputStream(commandTestFile)

    // noinspection RegExpSimplifiable
    def testLog(msg: String): Unit = {
      log.info(msg)
      val s = msg.replaceAll("Id\\([a-z0-9\\-]*\\)", "Id(test)")
      testFd.write(s"$s\n".getBytes())
    }

    val currentStateSubscription = pythonService.subscribeCurrentState { cs =>
      // make test reproducible
      val sortedParams = cs.paramSet.toList.sortBy(_.keyName)
      testLog(
        "Received current state from python service: " +
          s"prefix=${cs.prefix}, stateName=${cs.stateName}, paramSet=$sortedParams"
      )
    }

    try {
      val longRunningCommand = makeTestCommand("LongRunningCommand")
      val validateResponse =
        Await.result(pythonService.validate(longRunningCommand), 5.seconds)
      testLog(s"Response from validate command to ${pythonConnection.componentId.fullName}: $validateResponse")

      val firstCommandResponse =
        Await.result(pythonService.submit(longRunningCommand), 5.seconds)
      testLog(
        s"Initial response from submit of long running command to ${pythonConnection.componentId.fullName}: $firstCommandResponse"
      )
      val finalCommandResponse = Await.result(pythonService.queryFinal(firstCommandResponse.runId), 20.seconds)
      testLog(
        s"Final response from submit of long running command to ${pythonConnection.componentId.fullName}: $finalCommandResponse"
      )

      val simpleCommand = makeTestCommand("SimpleCommand")
      val simpleCommandResponse =
        Await.result(pythonService.submit(simpleCommand), 5.seconds)
      testLog(s"Response from simple submit to ${pythonConnection.componentId.fullName}: $simpleCommandResponse")

      // Test cancel of current state subscription
      currentStateSubscription.cancel()

      val resultCommand = makeTestCommand("ResultCommand")
      val resultCommandResponse =
        Await.result(pythonService.submit(resultCommand), 5.seconds)
      testLog(s"Response with result from submit to ${pythonConnection.componentId.fullName}: $resultCommandResponse")

      val errorCommand = makeTestCommand("ErrorCommand")
      val errorCommandResponse =
        Await.result(pythonService.submit(errorCommand), 5.seconds)
      testLog(s"Response from error command submit to ${pythonConnection.componentId.fullName}: $errorCommandResponse")

      val invalidCommand = makeTestCommand("InvalidCommand")
      val invalidCommandResponse =
        Await.result(pythonService.submit(invalidCommand), 5.seconds)
      testLog(s"Response from invalid command submit to ${pythonConnection.componentId.fullName}: $invalidCommandResponse")
    }
    catch {
      case e: Exception =>
        log.error("Error sending command to python test", ex = e)
    }
    // The python test exits after receiving the oneway command (otherwise it would just hang and never end).
    // Ignore the error that causes.
    try {
      val onewayCommand = makeTestCommand("OneWay")
      Await.ready(pythonService.oneway(onewayCommand), 5.seconds)
    }
    catch {
      case e: RuntimeException if e.getMessage.startsWith("The http server closed the connection unexpectedly") =>
      case e: Exception =>
        log.error("Error sending OneWay command to python test", ex = e)
    }
    testFd.close()
  }
}
