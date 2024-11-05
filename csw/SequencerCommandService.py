from csw.CommandResponse import SubmitResponse
from esw.Sequence import Sequence


class SequencerCommandService:

    def submit(self, sequence: Sequence) -> SubmitResponse:
        pass

    def submitAndWait(self, sequence: Sequence, timeoutInSeconds: int) -> SubmitResponse:
        pass

    def query(self, runId: str) -> SubmitResponse:
        pass

    def queryFinal(self, runId: str, timeoutInSeconds: int = 10) -> SubmitResponse:
        pass
