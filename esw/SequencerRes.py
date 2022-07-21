from dataclasses import dataclass
from enum import Enum


@dataclass
class SequencerRes:
    def _asDict(self):
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
        }

    @staticmethod
    def _fromDict(obj: dict):
        match obj["_type"]:
            case "Ok":
                return Ok()
            case "Unhandled":
                return Unhandled._fromDict(obj)
            case "IdDoesNotExist":
                return IdDoesNotExist()
            case "CannotOperateOnAnInFlightOrFinishedStep":
                return CannotOperateOnAnInFlightOrFinishedStep()
            case "GoOnlineHookFailed":
                return GoOnlineHookFailed()
            case "GoOfflineHookFailed":
                return GoOfflineHookFailed()
            case "DiagnosticHookFailed":
                return DiagnosticHookFailed()
            case "OperationsHookFailed":
                return OperationsHookFailed()


@dataclass
class Ok(SequencerRes):
    pass


@dataclass
class Unhandled(SequencerRes):
    state: str
    messageType: str
    msg: str

    def _asDict(self):
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "state": self.state,
            "messageType": self.messageType,
            "msg": self.msg,
        }

    @staticmethod
    def _fromDict(obj: dict):
        return Unhandled(obj["state"], obj["messageType"], obj["msg"])


@dataclass
class IdDoesNotExist(SequencerRes):
    pass


@dataclass
class CannotOperateOnAnInFlightOrFinishedStep(SequencerRes):
    pass


@dataclass
class GoOnlineHookFailed(SequencerRes):
    pass


@dataclass
class GoOfflineHookFailed(SequencerRes):
    pass


@dataclass
class DiagnosticHookFailed(SequencerRes):
    pass


@dataclass
class OperationsHookFailed(SequencerRes):
    pass


OkOrUnhandledResponse = Ok | Unhandled
GenericResponse = OkOrUnhandledResponse | IdDoesNotExist | CannotOperateOnAnInFlightOrFinishedStep
PauseResponse = OkOrUnhandledResponse | CannotOperateOnAnInFlightOrFinishedStep
RemoveBreakpointResponse = OkOrUnhandledResponse | IdDoesNotExist
GoOnlineResponse = OkOrUnhandledResponse | GoOnlineHookFailed
GoOfflineResponse = OkOrUnhandledResponse | GoOfflineHookFailed
DiagnosticModeResponse = Ok | DiagnosticHookFailed
OperationsModeResponse = Ok | OperationsHookFailed

class SequencerState(Enum):
    Idle = 1
    Processing = 2
    Loaded = 3
    Offline = 4
    Running = 5