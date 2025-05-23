from datetime import timedelta
from typing import Callable, List, Awaitable

import structlog
from aiohttp import ClientSession

from csw.CommandResponse import ValidateResponse, OnewayResponse, SubmitResponse
from csw.CommandService import CommandService, Subscription
from csw.CurrentState import CurrentState
from csw.LocationService import ComponentType
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
from csw.TMTTime import UTCTime


class RichComponent:

    def __init__(self, prefix: Prefix,
                 componentType: ComponentType,
                 clientSession: ClientSession,
                 # lockUnlockUtil: LockUnlockUtil
                 # commandUtil: CommandUtil
                 defaultTimeout: timedelta):
        self.prefix = prefix
        self.componentType = componentType
        self.clientSession = clientSession
        self.defaultTimeout = defaultTimeout
        self.log = structlog.get_logger()

    def commandService(self) -> CommandService:
        return CommandService(self.prefix, self.componentType, self.clientSession)

    async def actionOnResponse(self, func: Callable[[], Awaitable[SubmitResponse]],
                               resumeOnError: bool = False) -> SubmitResponse:
        if not resumeOnError:
            return (await func()).onFailedTerminate()
        else:
            return await func()

    async def validate(self, command: ControlCommand) -> ValidateResponse:
        """
        Sends validate command to component. Returns the ValidateResponse can be of type Accepted, Invalid
        or Locked.

        Args:
            command the ControlCommand payload
        """
        return await self.commandService().validate(command)

    async def oneway(self, command: ControlCommand) -> OnewayResponse:
        """
        Send a command as a Oneway and get a [[csw.params.commands.CommandResponse.OnewayResponse]]. The CommandResponse can be a response
        of validation (Accepted, Invalid), or a Locked response.

        Args:
            command the ControlCommand payload
        """
        return await self.commandService().oneway(command)

    async def submit(self, command: ControlCommand, resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a command to assembly/hcd and return after first phase. If it returns as `Started` get a
        final SubmitResponse as a Future with queryFinal.

        Args:
            command the ControlCommand payload
            resumeOnError script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """

        async def f():
            return await self.commandService().submit(command)

        return await self.actionOnResponse(f, resumeOnError)

    async def query(self, commandRunId: str, resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the result of a long-running command which was sent as Submit to get a [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            commandRunId: the runId of the command for which response is required
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """

        async def f():
            return await self.commandService().query(commandRunId)

        return await self.actionOnResponse(f, resumeOnError)

    def _defaultTimeout(self, t: timedelta | None) -> timedelta:
        if t:
            return t
        else:
            return self.defaultTimeout

    async def queryFinal(self, commandRunId: str, timeout: timedelta | None = None,
                         resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the final result of a long-running command which was sent as Submit to get a [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            commandRunId: the runId of the command for which response is required
            timeout: duration for which api will wait for final response, if command is not completed queryFinal will timeout
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """

        async def f():
            return await self.commandService().queryFinal(commandRunId, self._defaultTimeout(timeout))

        return await self.actionOnResponse(f, resumeOnError)

    def submitAndWait(self, command: ControlCommand, timeout: timedelta | None = None,
                      resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a command and wait for the final result if it was successfully validated as `Started` to get a
        final [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            command: the [[csw.params.commands.ControlCommand]] payload
            timeout: duration for which api will wait for final response, if command is not completed queryFinal will time out
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """

        async def f():
            return await self.commandService().submitAndWait(command, self._defaultTimeout(timeout))

        return self.actionOnResponse(f, resumeOnError)

    async def subscribeCurrentState(self, stateNames: List[str], callback: Callable[[CurrentState], Awaitable]) -> Subscription:
        """
        Subscribe to the current state of a component

        Args:
            stateNames: subscribe to only those states which have any of the provided value for name
            callback: the action to be applied on the CurrentState element received as a result of subscription

        Returns:
            a Subscription to stop the subscription
        """
        return await self.commandService().subscribeCurrentState(stateNames, callback)

    async def diagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Send component into a diagnostic data mode based on a hint at the specified startTime.

        Args:
            startTime represents the time at which the diagnostic mode actions will take effect
            hint represents supported diagnostic data mode for a component
        """
        await self.commandService().executeDiagnosticMode(startTime, hint)

    async def operationsMode(self):
        """
        Send component into an operations mode
        """
        await self.commandService().executeOperationsMode()

    async def goOnline(self):
        """
        Send component into online mode
        """
        await self.commandService().goOnline()

    async def goOffline(self):
        """
        Send component into offline mode
        """
        await self.commandService().goOffline()

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
