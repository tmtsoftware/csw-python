from dataclasses import dataclass

from csw.ParameterSetType import SequenceCommand
from esw.StepStatus import StepStatus


# noinspection PyProtectedMember
@dataclass
class Step:
    id: str
    command: SequenceCommand
    status: StepStatus
    hasBreakpoint: bool

    def _asDict(self) -> dict:
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "id": self.id,
            "command": self.command._asDict(),
            "status": self.status._asDict(),
            "hasBreakpoint": str(self.hasBreakpoint).lower()
        }

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        id = obj["id"]
        command = SequenceCommand._fromDict(obj["command"])
        status = StepStatus._fromDict(obj["status"])
        hasBreakpoint = obj["hasBreakpoint"]
        return Step(id, command, status, hasBreakpoint)
