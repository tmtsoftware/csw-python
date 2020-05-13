package org.tmt.csw.testassembly

import java.io.{File, FileOutputStream}
import java.time.Instant

import akka.actor.typed.{ActorSystem, Behavior}
import akka.actor.typed.scaladsl.{ActorContext, Behaviors}
import csw.command.client.messages.TopLevelActorMessage
import csw.framework.models.CswContext
import csw.framework.scaladsl.ComponentHandlers
import csw.location.api.models.{
  ComponentId,
  ComponentType,
  Location,
  LocationRemoved,
  LocationUpdated,
  TrackingEvent
}
import csw.logging.api.scaladsl.Logger
import csw.params.commands.CommandResponse._
import csw.params.commands.{CommandName, ControlCommand, Setup}
import csw.time.core.models.UTCTime
import csw.params.core.models.{Angle, Coords, Id, ProperMotion, Struct}
import csw.params.events.{Event, EventKey, EventName, SystemEvent}
import csw.params.core.formats.ParamCodecs._

import scala.concurrent.{Await, ExecutionContextExecutor, Future}
import TestAssemblyHandlers._
import akka.util.Timeout
import csw.command.client.CommandServiceFactory
import csw.location.api.models.Connection.HttpConnection
import csw.params.core.generics.{Key, KeyType}
import csw.params.core.generics.KeyType.CoordKey
import csw.params.core.models.Coords.EqFrame.FK5
import csw.params.core.models.Coords.SolarSystemObject.Venus
import csw.prefix.models.Prefix
import csw.prefix.models.Subsystem.CSW
import io.bullet.borer.Json

import scala.concurrent.duration._

object TestAssemblyHandlers {

  // Event published by C code and subscribed to here
  private val prefix = Prefix(CSW, "TestPublisher")
  private val eventNames = List(
    "testEvent1",
    "testEvent2",
    "testEvent3"
  ).map(EventName).toSet
  private val eventKeys = eventNames.map(EventKey(prefix, _))

  // Generate a test file with the JSON for the received events, as an easy way to compare with the expected values
  private val eventTestFile = new File("/tmp/PyTestAssemblyEventHandlers.out")

  // Actor to receive events
  private def eventHandler(log: Logger): Behavior[Event] = {
    def handleEvent(event: SystemEvent): Unit = {
      log.info(s"Received event: $event")
      if (event.eventName.name.startsWith("testEvent")) {
        // Check that event time is recent
        // Create the file when the first event is received from the test, close it on the last
        val append = event.eventName.name != "testEvent1"
        val testFd = new FileOutputStream(eventTestFile, append)
        val ev: Event = event.copy(
          eventId = Id("test"),
          eventTime = UTCTime(Instant.ofEpochSecond(0)))
        val json = Json.encode(ev).toUtf8String + "\n"
        testFd.write(json.getBytes)
        log.info(s"XXX Writing to $eventTestFile")
        testFd.close()
      }
    }

    Behaviors.receive { (_, msg) =>
      msg match {
        case event: SystemEvent =>
          log.info(s"received event: $event")
          try {
            handleEvent(event)
          } catch {
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
class TestAssemblyHandlers(ctx: ActorContext[TopLevelActorMessage],
                           cswCtx: CswContext)
    extends ComponentHandlers(ctx, cswCtx) {

  import cswCtx._

  implicit val system: ActorSystem[Nothing] = ctx.system
  implicit val ec: ExecutionContextExecutor = ctx.executionContext

  implicit def timeout: Timeout = new Timeout(20.seconds)

  private val log = loggerFactory.getLogger
  // See tests/test_commands_with_assembly.py
  private val pythonConnection = HttpConnection(
    ComponentId(Prefix(CSW, "pycswTest"), ComponentType.Service))

  override def initialize(): Future[Unit] = {
    log.info("Initializing test assembly...")
    startSubscribingToEvents()
    Future.unit
  }

  private def startSubscribingToEvents(): Unit = {
    val eventHandlerActor = ctx.spawn(eventHandler(log), "eventHandlerActor")
    eventService.defaultSubscriber
      .subscribeActorRef(eventKeys, eventHandlerActor)
  }

  override def onLocationTrackingEvent(trackingEvent: TrackingEvent): Unit = {
    trackingEvent match {
      case LocationUpdated(location)
          if location.connection == pythonConnection =>
        sendCommandsToPython(location)
      case LocationRemoved(connection) if connection == pythonConnection =>
        log.info(s"XXX python based service was removed from Location Service")
      case _ =>
    }
  }

  override def validateCommand(
      runId: Id,
      controlCommand: ControlCommand): ValidateCommandResponse = Accepted(runId)

  override def onSubmit(runId: Id,
                        controlCommand: ControlCommand): SubmitResponse =
    Completed(runId)

  override def onOneway(runId: Id, controlCommand: ControlCommand): Unit = {}

  override def onShutdown(): Future[Unit] = {
    Future.unit
  }

  override def onGoOffline(): Unit = {}

  override def onGoOnline(): Unit = {}

  override def onDiagnosticMode(startTime: UTCTime, hint: String): Unit = {}

  override def onOperationsMode(): Unit = {}

  // Dummy test command
  private def makeTestCommand(commandName: String): ControlCommand = {
    import Angle._
    import Coords._

    val basePosKey = CoordKey.make("BasePosition")
    val cmdKey1: Key[Float] = KeyType.FloatKey.make("cmdValue")
    val cmdKey1b: Key[Float] = KeyType.FloatKey.make("cmdValue")
    val cmdKey2b: Key[Struct] =
      KeyType.StructKey.make("cmdStructValueB")
    val cmdKey3: Key[Int] =
      KeyType.IntKey.make("cmdStructValue3")
    val cmdKey4: Key[Byte] =
      KeyType.ByteKey.make("cmdStructValue4")

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

    Setup(componentInfo.prefix, CommandName(commandName), None)
      .add(posParam)
      .add(cmdKey1b.set(1.0f, 2.0f, 3.0f))
      .add(
        cmdKey2b.set(
          Struct()
            .add(cmdKey1.set(1.0f))
            .add(cmdKey3.set(1, 2, 3)),
          Struct()
            .add(cmdKey1.set(2.0f))
            .add(cmdKey3.set(4, 5, 6))
            .add(cmdKey4.set(9.toByte, 10.toByte))
        )
      )
  }

  // Send some test commands to the python based command service
  // See tests/test_commands_with_assembly.py.
  private def sendCommandsToPython(location: Location): Unit = {
    log.info(s"XXX python based service is located: $location")
    val pythonService = CommandServiceFactory.make(location)
    try {
      val longRunningCommand = makeTestCommand("LongRunningCommand")
      val validateResponse =
        Await.result(pythonService.validate(longRunningCommand), 5.seconds)
      log.info(
        s"Response from validate command to ${pythonConnection.componentId.fullName}: $validateResponse")

      val firstCommandResponse =
        Await.result(pythonService.submit(longRunningCommand), 5.seconds)
      log.info(
        s"Initial response from submit of long running command to ${pythonConnection.componentId.fullName}: $firstCommandResponse")
      val finalCommandResponse = Await.result(
        pythonService.queryFinal(firstCommandResponse.runId),
        20.seconds)
      log.info(
        s"Final response from submit of long running command to ${pythonConnection.componentId.fullName}: $finalCommandResponse")

      val simpleCommand = makeTestCommand("SimpleCommand")
      val simpleCommandResponse =
        Await.result(pythonService.submit(simpleCommand), 5.seconds)
      log.info(
        s"Response from simple submit to ${pythonConnection.componentId.fullName}: $simpleCommandResponse")

      val resultCommand = makeTestCommand("ResultCommand")
      val resultCommandResponse =
        Await.result(pythonService.submit(resultCommand), 5.seconds)
      log.info(
        s"Response with result from submit to ${pythonConnection.componentId.fullName}: $resultCommandResponse")

      val errorCommand = makeTestCommand("ErrorCommand")
      val errorCommandResponse =
        Await.result(pythonService.submit(errorCommand), 5.seconds)
      log.info(
        s"Response from error command submit to ${pythonConnection.componentId.fullName}: $errorCommandResponse")

      val invalidCommand = makeTestCommand("InvalidCommand")
      val invalidCommandResponse =
        Await.result(pythonService.submit(invalidCommand), 5.seconds)
      log.info(
        s"Response from invalid command submit to ${pythonConnection.componentId.fullName}: $invalidCommandResponse")
    } catch {
      case e: Exception =>
        log.error("Error sending command to python test", ex = e)
    }
    // The python test exits after receiving the oneway command (otherwise it would just hang and never end).
    // Ignore the error that causes.
    try {
      val onewayCommand = makeTestCommand("OneWay")
      val onewayResponse =
        Await.result(pythonService.oneway(onewayCommand), 5.seconds)
      log.info(
        s"Response from oneway command to ${pythonConnection.componentId.fullName}: $onewayResponse")
    } catch {
      case e: RuntimeException
          if e.getMessage.startsWith(
            "The http server closed the connection unexpectedly") =>
      case e: Exception =>
        log.error("Error sending command to python test", ex = e)
    }
  }
}
