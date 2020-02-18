package org.tmt.csw.testhcd

import akka.actor.typed.scaladsl.ActorContext
import csw.command.client.messages.TopLevelActorMessage
import csw.framework.models.CswContext
import csw.framework.scaladsl.ComponentHandlers
import csw.location.api.models.TrackingEvent
import csw.params.commands.CommandResponse._
import csw.params.commands.ControlCommand
import csw.time.core.models.UTCTime
import csw.params.core.models.Id

import scala.concurrent.{ExecutionContextExecutor, Future}

/**
  * Domain specific logic should be written in below handlers.
  * This handlers gets invoked when component receives messages/commands from other component/entity.
  * For example, if one component sends Submit(Setup(args)) command to TestHcd,
  * This will be first validated in the supervisor and then forwarded to Component TLA which first invokes validateCommand hook
  * and if validation is successful, then onSubmit hook gets invoked.
  * You can find more information on this here : https://tmtsoftware.github.io/csw/commons/framework.html
  */
class TestHcdHandlers(ctx: ActorContext[TopLevelActorMessage],
                      cswCtx: CswContext)
    extends ComponentHandlers(ctx, cswCtx) {

  import cswCtx._
  implicit val ec: ExecutionContextExecutor = ctx.executionContext
  private val log = loggerFactory.getLogger

  override def initialize(): Future[Unit] = {
    log.info("Initializing test HCD...")
    Future.unit
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
