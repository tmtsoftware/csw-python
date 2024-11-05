from csw.SequencerCommandService import SequencerCommandService
from csw.UTCTime import UTCTime
from esw.EswSequencerResponse import OkOrUnhandledResponse, PullNextResponse, MaybeNextResponse, DiagnosticModeResponse, \
    OperationsModeResponse, GoOnlineResponse, GoOfflineResponse


class SequencerApi(SequencerCommandService):
    def pullNext(self) -> PullNextResponse:
        pass

    def maybeNext(self) -> MaybeNextResponse:
        pass

    def readyToExecuteNext(self) -> OkOrUnhandledResponse:
        pass

    def stepSuccess(self):
        pass

    def stepFailure(self, message: str):
        pass
    
    def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        """
        Sends command to the sequencer to call the diagnostic mode handler of the sequencer's script
        Args:
        startTime: time at which the diagnostic mode will take effect
        hint: String to support diagnostic data mode
        """
        pass

    def operationsMode(self) -> OperationsModeResponse:
        """
        Sends command to the sequencer to call the operations mode handler of the sequencer's script
        """
        pass

    def goOnline(self) -> GoOnlineResponse:
        """
        sends command to the sequencer to go in Online state if it is in Offline state
        """
        pass

    def goOffline(self) -> GoOfflineResponse:
        """
        sends command to the sequencer to go in Offline state if it is in Online state
        """
        pass

    def abortSequence(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the abort handler of the sequencer's script
        """
        pass

    def stop(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the stop handler of the sequencer's script
        """
        pass

