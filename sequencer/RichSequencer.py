from attr import dataclass

from csw.CommandResponse import SubmitResponse, CommandError
from csw.Subsystem import Subsystem
from csw.UTCTime import UTCTime
from esw.EswSequencerResponse import GoOnlineResponse, GoOfflineResponse, DiagnosticModeResponse, \
    OperationsModeResponse, OkOrUnhandledResponse
from esw.ObsMode import ObsMode
from esw.Sequence import Sequence
from esw.SequencerClient import SequencerClient
from esw.Variation import Variation
from sequencer.SequencerApi import SequencerApi


@dataclass
class RichSequencer:
    subsystem: Subsystem
    obsMode: ObsMode
    variation: Variation | None
    defaultTimeoutInSeconds: int

    def _sequencerApiFactory(self) -> SequencerApi:
        return SequencerClient(Variation.prefix(self.subsystem, self.obsMode, self.variation))

    def _sequencerService(self):
        return self._sequencerApiFactory()

    async def submit(self, sequence: Sequence, resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a sequence to the sequencer and return the immediate response If it returns as `Started` get a
        final SubmitResponse as a Future with queryFinal.

        Args:
            sequence: the Sequence payload
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        submitResponse = await self._sequencerService().submit(sequence)
        if not resumeOnError and submitResponse.isFailed:
            raise CommandError(submitResponse)
        return submitResponse

    async def query(self, runId: str, resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the result of a long running command which was sent as Submit to get a [[csw.params.commands.CommandResponse.SubmitResponse]]

        Args:
            runId: the runId of the sequence for which response is required
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        submitResponse = await self._sequencerService().query(runId)
        if not resumeOnError and submitResponse.isFailed:
            raise CommandError(submitResponse)
        return submitResponse

    async def queryFinal(self, runId: str, timeoutInSeconds: int, resumeOnError: bool = False) -> SubmitResponse:
        """
        Query for the final result of a long running sequence which was sent as Submit to get a SubmitResponse
        Args:
            runId: the runId of the sequence for which response is required
            timeout: duration for which api will wait for final response, if command is not completed queryFinal will timeout
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        submitResponse = await self._sequencerService().queryFinal(runId)
        if not resumeOnError and submitResponse.isFailed:
            raise CommandError(submitResponse)
        return submitResponse

    async def submitAndWait(self, sequence: Sequence, timeoutInSeconds: int = 10, resumeOnError: bool = False) -> SubmitResponse:
        """
        Submit a sequence and wait for the final result to get a final SubmitResponse

        Args:
            sequence: the Sequence payload
            timeoutInSeconds: duration for which api will wait for final response
            resumeOnError: script execution continues if set true. If false, script execution flow breaks and sequence in
            execution completes with failure.
        """
        submitResponse = await self._sequencerService().submitAndWait(sequence, timeoutInSeconds)
        if not resumeOnError and submitResponse.isFailed():
            raise CommandError(submitResponse)
        return submitResponse

    async def goOnline(self) -> GoOnlineResponse:
        """
        Sends the sequencer in Online Mode if it is Offline and executes the onGoOnline handler of the script
        """
        return await self._sequencerService().goOnline()

    async def goOffline(self) -> GoOfflineResponse:
        """
        Sends the sequencer in Offline Mode if it is Online and executes the onGoOffline handler of the script
        """
        return await self._sequencerService().goOffline()

    async def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        """
        Runs the onDiagnosticMode handler of script

        Args:
            startTime: startTime argument for the diagnostic handler
            hint: hint argument for the diagnostic handler
        """
        return await self._sequencerService().diagnosticMode(startTime, hint)

    async def operationsMode(self) -> OperationsModeResponse:
        """
        Runs the onOperationsMode handler of script
        """
        return await self._sequencerService().operationsMode()

    async def abortSequence(self) -> OkOrUnhandledResponse:
        """
        Aborts the running sequence in the sequencer by discarding all the pending steps and runs the onAbortSequence handler of the script
        """
        return await self._sequencerService().abortSequence()

    async def stop(self) -> OkOrUnhandledResponse:
        """
        Stops the running sequence in the sequencer by discarding all the pending steps and runs the onStop handler of the script
        """
        return await self._sequencerService().stop()
