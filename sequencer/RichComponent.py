from dataclasses import dataclass
from typing import Callable

from csw.CommandResponse import ValidateResponse, OnewayResponse, SubmitResponse
from csw.CommandService import CommandService, Subscription
from csw.CommandServiceRequest import StateName
from csw.CurrentState import CurrentState
from csw.LocationService import ComponentType
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
from csw.UTCTime import UTCTime


@dataclass
class RichComponent:
    prefix: Prefix
    componentType: ComponentType
    # lockUnlockUtil: LockUnlockUtil
    # commandUtil: CommandUtil
    defaultTimeoutInSeconds: int

    def commandService(self) -> CommandService:
        return CommandService(self.prefix, self.componentType)

    def actionOnResponse(self, func: Callable[[], SubmitResponse], resumeOnError: bool = False) -> SubmitResponse:
        if not resumeOnError:
            func().onFailedTerminate()
        else:
            func()

    def validate(self, command: ControlCommand) -> ValidateResponse:
        """
        Sends validate command to component. Returns the ValidateResponse can be of type Accepted, Invalid
        or Locked.

        Args:
            command the ControlCommand payload
        """
        self.commandService().validate(command)

    def oneway(self, command: ControlCommand) -> OnewayResponse:
        """
        Send a command as a Oneway and get a [[csw.params.commands.CommandResponse.OnewayResponse]]. The CommandResponse can be a response
        of validation (Accepted, Invalid), or a Locked response.

        Args:
            command the ControlCommand payload
        """
        self.commandService().oneway(command)

    def submit(self, command: ControlCommand, resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a command to assembly/hcd and return after first phase. If it returns as `Started` get a
        final SubmitResponse as a Future with queryFinal.

        Args:
            command the ControlCommand payload
            resumeOnError script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        return self.actionOnResponse(lambda: self.commandService().submit(command), resumeOnError)

    def query(self, commandRunId: str, resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the result of a long running command which was sent as Submit to get a [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            commandRunId: the runId of the command for which response is required
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        return self.actionOnResponse(lambda: self.commandService().query(commandRunId), resumeOnError)

    def queryFinal(self, commandRunId: str, timeoutInSecs: int = 10, resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the final result of a long running command which was sent as Submit to get a [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            commandRunId: the runId of the command for which response is required
            timeout: duration for which api will wait for final response, if command is not completed queryFinal will timeout
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        self.actionOnResponse(lambda: self.commandService().queryFinal(commandRunId, timeoutInSecs), resumeOnError)

    def submitAndWait(self, command: ControlCommand, timeoutInSecs: int = 10,
                      resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a command and wait for the final result if it was successfully validated as `Started` to get a
        final [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            command: the [[csw.params.commands.ControlCommand]] payload
            timeout: duration for which api will wait for final response, if command is not completed queryFinal will timeout
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        return self.actionOnResponse(lambda: self.commandService().submitAndWait(command, timeoutInSecs), resumeOnError)

    def subscribeCurrentState(self, *stateNames: str, callback: Callable[[CurrentState], None]) -> Subscription:
        """
        Subscribe to the current state of a component

        Args:
            stateNames: subscribe to only those states which have any of the provided value for name
            callback: the action to be applied on the CurrentState element received as a result of subscription

        Returns:
            a Subscription to stop the subscription
        """
        return self.commandService().subscribeCurrentState(list(stateNames), callback)

    # XXX TODO FIXME: Need to add HTTP API for these?

    def diagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Send component into a diagnostic data mode based on a hint at the specified startTime.

        Args:
            startTime represents the time at which the diagnostic mode actions will take effect
            hint represents supported diagnostic data mode for a component
        """
        self.commandService().executeDiagnosticMode(startTime, hint)

    def operationsMode(self):
        """
        Send component into an operations mode
        """
        self.commandService().executeOperationsMode()

    def goOnline(self):
        """
        Send component into online mode
        """
        self.commandService().goOnline()

    def goOffline(self):
        """
        Send component into offline mode
        """
        self.commandService().goOnline()

        #     /**
        #      * Lock component for specified duration. Returns [[csw.command.client.models.framework.LockingResponse.LockAcquired]]
        #      * or [[csw.command.client.models.framework.LockingResponse.AcquiringLockFailed]]
        #      * @param leaseDuration duration for which component needs to be locked
        #      * @param onLockAboutToExpire callback which will be executed when Lock is about to expire
        #      * @param onLockExpired callback which will be executed when Lock is about to expire
        #      * @return return LockingResponse
        #      */
        #     suspend fun lock(
        #             leaseDuration: Duration,
        #             onLockAboutToExpire: SuspendableCallback = {},
        #             onLockExpired: SuspendableCallback = {}
        #     ): LockingResponse =
        #             lockUnlockUtil.lock(
        #                     componentRef(),
        #                     leaseDuration.toJavaDuration(),
        #                     { onLockAboutToExpire.toJava() },
        #                     { onLockExpired.toJava() }
        #             ).await()
        #
        #     /**
        #      * Unlocks component. Returns [[csw.command.client.models.framework.LockingResponse.LockReleased]]
        #      * or [[csw.command.client.models.framework.LockingResponse.LockAlreadyReleased]] or [[csw.command.client.models.framework.LockingResponse.ReleasingLockFailed]]
        #      *
        #      * @return LockingResponse
        #      */
        #     suspend fun unlock(): LockingResponse = lockUnlockUtil.unlock(componentRef()).await()
