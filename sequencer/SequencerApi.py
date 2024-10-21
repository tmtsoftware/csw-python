from esw.EswSequencerResponse import OkOrUnhandledResponse, PullNextResponse, MaybeNextResponse


class SequencerApi:
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
