from csw.CommandResponse import SubmitResponse
from esw.Sequence import Sequence


class SequencerCommandService:

    async def submit(self, sequence: Sequence) -> SubmitResponse:
        pass

    async def submitAndWait(self, sequence: Sequence, timeoutInSeconds: int) -> SubmitResponse:
        pass

    async def query(self, runId: str) -> SubmitResponse:
        pass

    async def queryFinal(self, runId: str, timeoutInSeconds: int = 10) -> SubmitResponse:
        pass
