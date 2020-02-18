package org.tmt.csw.testassembly;

import akka.actor.typed.javadsl.ActorContext;
import csw.command.client.messages.TopLevelActorMessage;
import csw.framework.javadsl.JComponentHandlers;
import csw.framework.models.JCswContext;
import csw.location.api.models.TrackingEvent;
import csw.logging.api.javadsl.ILogger;
import csw.params.commands.CommandResponse;
import csw.params.commands.ControlCommand;
import csw.time.core.models.UTCTime;
import csw.params.core.models.Id;

import java.util.concurrent.CompletableFuture;

/**
 * Domain specific logic should be written in below handlers.
 * This handlers gets invoked when component receives messages/commands from other component/entity.
 * For example, if one component sends Submit(Setup(args)) command to TestHcd,
 * This will be first validated in the supervisor and then forwarded to Component TLA which first invokes validateCommand hook
 * and if validation is successful, then onSubmit hook gets invoked.
 * You can find more information on this here : https://tmtsoftware.github.io/csw/commons/framework.html
 */
public class JTestAssemblyHandlers extends JComponentHandlers {

    private final JCswContext cswCtx;
    private final ILogger log;

    JTestAssemblyHandlers(ActorContext<TopLevelActorMessage> ctx,JCswContext cswCtx) {
        super(ctx, cswCtx);
        this.cswCtx = cswCtx;
        this.log = cswCtx.loggerFactory().getLogger(getClass());
    }

    @Override
    public CompletableFuture<Void> jInitialize() {
    log.info("Initializing test assembly...");
    return CompletableFuture.runAsync(() -> {

        });
    }

    @Override
    public CompletableFuture<Void> jOnShutdown() {
        return CompletableFuture.runAsync(() -> {

        });
    }

    @Override
    public void onLocationTrackingEvent(TrackingEvent trackingEvent) {

    }

    @Override
    public CommandResponse.ValidateCommandResponse validateCommand(Id runId, ControlCommand controlCommand) {
        return new CommandResponse.Accepted(runId);
    }

    @Override
    public CommandResponse.SubmitResponse onSubmit(Id runId, ControlCommand controlCommand) {
        return new CommandResponse.Completed(runId);
    }

    @Override
    public void onOneway(Id runId, ControlCommand controlCommand) {

    }

    @Override
    public void onGoOffline() {

    }

    @Override
    public void onGoOnline() {

    }

    @Override
    public void onDiagnosticMode(UTCTime startTime,String hint){

    }

    @Override
    public void onOperationsMode(){

    }
}
