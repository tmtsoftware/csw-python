package org.tmt.csw.testassembly

import java.io.{File, FileOutputStream}
import java.time.Instant

import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.{ActorContext, Behaviors}
import csw.command.client.messages.TopLevelActorMessage
import csw.framework.models.CswContext
import csw.framework.scaladsl.ComponentHandlers
import csw.location.api.models.TrackingEvent
import csw.logging.api.scaladsl.Logger
import csw.params.commands.CommandResponse._
import csw.params.commands.ControlCommand
import csw.time.core.models.UTCTime
import csw.params.core.models.Id
import csw.params.events.{Event, EventKey, EventName, SystemEvent}
import csw.params.core.formats.JsonSupport
import csw.params.core.formats.ParamCodecs._

import scala.concurrent.{ExecutionContextExecutor, Future}
import TestAssemblyHandlers._
import csw.prefix.models.Prefix
import csw.prefix.models.Subsystem.CSW
import io.bullet.borer.Json

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
  private val testFile = new File("/tmp/PyTestAssemblyHandlers.out")
  private var testFd: Option[FileOutputStream] = None
  private var eventCount = 0;

  // Actor to receive events
  private def eventHandler(log: Logger): Behavior[Event] = {
    def handleEvent(event: SystemEvent): Unit = {
      // Check that event time is recent
      if (UTCTime
            .now()
            .value
            .getEpochSecond - event.eventTime.value.getEpochSecond < 5) {
        // Create the file when the first event is received from the test, close it on the last
        if (eventCount == 0) {
          testFd.foreach(_.close())
          testFd = Some(new FileOutputStream(testFile))
        }
        eventCount = eventCount + 1
        val ev: Event = event.copy(
          eventId = Id("test"),
          eventTime = UTCTime(Instant.ofEpochSecond(0)))
        val json = Json.encode(ev).toUtf8String + "\n"
        testFd.foreach(_.write(json.getBytes))
        if (testFd.isEmpty)
          log.warn(s"Can't save $event")

        if (eventCount == eventNames.size) {
          testFd.foreach(_.close())
          testFd = None
          eventCount = 0
        }
      } else {
        log.warn(
          s"Event is too old: UTC Now: ${UTCTime.now().value}, Event Time: ${event.eventTime.value}")
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
  implicit val ec: ExecutionContextExecutor = ctx.executionContext
  private val log = loggerFactory.getLogger

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

  override def onLocationTrackingEvent(trackingEvent: TrackingEvent): Unit = {}

  override def validateCommand(
      runId: Id,
      controlCommand: ControlCommand): ValidateCommandResponse = Accepted(runId)

  override def onSubmit(runId: Id,
                        controlCommand: ControlCommand): SubmitResponse =
    Completed(runId)

  override def onOneway(runId: Id, controlCommand: ControlCommand): Unit = {}

  override def onShutdown(): Future[Unit] = { Future.unit }

  override def onGoOffline(): Unit = {}

  override def onGoOnline(): Unit = {}

  override def onDiagnosticMode(startTime: UTCTime, hint: String): Unit = {}

  override def onOperationsMode(): Unit = {}

}
