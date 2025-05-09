from dataclasses import dataclass
from enum import Enum
from typing import Self

from esw.Step import Step


@dataclass
class EswSequencerResponse:
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
            case "PullNextResult":
                return PullNextResult._fromDict(obj)
            case "MaybeNextResult":
                return MaybeNextResult._fromDict(obj)


@dataclass
class Ok(EswSequencerResponse):
    pass


@dataclass
class Unhandled(EswSequencerResponse):
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
class IdDoesNotExist(EswSequencerResponse):
    pass


@dataclass
class CannotOperateOnAnInFlightOrFinishedStep(EswSequencerResponse):
    pass


@dataclass
class GoOnlineHookFailed(EswSequencerResponse):
    pass


@dataclass
class GoOfflineHookFailed(EswSequencerResponse):
    pass


@dataclass
class DiagnosticHookFailed(EswSequencerResponse):
    pass


@dataclass
class OperationsHookFailed(EswSequencerResponse):
    pass


# --- For script use ---
@dataclass
class MaybeNextResult(EswSequencerResponse):
    maybeStep: Step | None

    @classmethod
    def _fromDict(cls, obj: dict) -> Self:
        if "maybeStep" in obj:
            return cls(Step._fromDict(obj["maybeStep"]))
        return cls(None)


@dataclass
class PullNextResult(EswSequencerResponse):
    step: Step

    @classmethod
    def _fromDict(cls, obj: dict) -> Self:
        return cls(Step._fromDict(obj["step"]))


PullNextResponse = PullNextResult | Unhandled
MaybeNextResponse = MaybeNextResult | Unhandled
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
