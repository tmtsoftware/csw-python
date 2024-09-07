from csw.CommandResponse import SubmitResponse


class ScriptError(Exception):
    def __init__(self, reason: str, throwable: Exception = None):
        super().__init__(reason)
        self.reason = reason
        self.throwable = throwable


class CommandError(ScriptError):
    def __init__(self, submitResponse: SubmitResponse):
        super().__init__(submitResponse.message)


class OtherError(ScriptError):
    def __init__(self, throwable: Exception):
        super().__init__(str(throwable), throwable)
