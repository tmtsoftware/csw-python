
class ScriptError(Exception):
    def __init__(self, reason: str, throwable: Exception = None):
        super().__init__(reason)
        self.reason = reason
        self.throwable = throwable


class OtherError(ScriptError):
    def __init__(self, throwable: Exception):
        super().__init__(str(throwable), throwable)
