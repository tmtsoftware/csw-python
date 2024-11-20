from csw.SequencerCommandService import SequencerCommandService
from csw.UTCTime import UTCTime
from esw.EswSequencerResponse import OkOrUnhandledResponse, PullNextResponse, MaybeNextResponse, DiagnosticModeResponse, \
    OperationsModeResponse, GoOnlineResponse, GoOfflineResponse


class SequencerApi(SequencerCommandService):
    async def pullNext(self) -> PullNextResponse:
        pass

    async def maybeNext(self) -> MaybeNextResponse:
        pass

    async def readyToExecuteNext(self) -> OkOrUnhandledResponse:
        pass

    async def stepSuccess(self):
        pass

    async def stepFailure(self, message: str):
        pass

    async def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        """
        Sends command to the sequencer to call the diagnostic mode handler of the sequencer's script
        Args:
        startTime: time at which the diagnostic mode will take effect
        hint: String to support diagnostic data mode
        """
        pass

    async def operationsMode(self) -> OperationsModeResponse:
        """
        Sends command to the sequencer to call the operations mode handler of the sequencer's script
        """
        pass

    async def goOnline(self) -> GoOnlineResponse:
        """
        sends command to the sequencer to go in Online state if it is in Offline state
        """
        pass

    async def goOffline(self) -> GoOfflineResponse:
        """
        sends command to the sequencer to go in Offline state if it is in Online state
        """
        pass

    async def abortSequence(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the abort handler of the sequencer's script
        """
        pass

    async def stop(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the stop handler of the sequencer's script
        """
        pass

