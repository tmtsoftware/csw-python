import traceback
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from dataclasses_json import dataclass_json

from csw.ParameterSetType import ControlCommand
from csw.TMTTime import UTCTime


@dataclass_json
@dataclass
class CommandServiceRequest:
    """
    Represents a command that requires a response (of type CommandResponse).

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand

    def _asDict(self):
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'controlCommand': self.controlCommand._asDict(),
        }


@dataclass_json
@dataclass
class Validate(CommandServiceRequest):
    pass


@dataclass_json
@dataclass
class Submit(CommandServiceRequest):
    pass


@dataclass_json
@dataclass
class Oneway(CommandServiceRequest):
    pass


@dataclass
class QueryFinal:
    """
    A message sent to query the final result of a long-running command.
    The response should be a CommandResponse.

    Args:
        runId (str): The command's runId
        timeout (timedelta) amount of time to wait
    """
    runId: str
    timeout: timedelta

    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        try:
            runId = obj['runId']
            timeout = timedelta(seconds=obj['timeoutInSeconds'])
            return QueryFinal(runId, timeout)
        except:
            traceback.print_exc()

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'timeoutInSeconds': int(self.timeout.total_seconds())
        }


@dataclass_json
@dataclass
class StateName:
    name: str


@dataclass
class SubscribeCurrentState:
    """
    Message used to subscribe to the current state of a component.

    Args:
        stateNames (List[str]) list of current state names to subscribe to
    """
    stateNames: List[str]

    @staticmethod
    def _fromDict(obj):
        """
        Returns a SubscribeCurrentState for the given dict.
        """
        if "names" in obj.keys():
            stateNames = obj.get("names")
        else:
            stateNames = []
        return SubscribeCurrentState(stateNames)

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'names': self.stateNames
        }


@dataclass
class ExecuteDiagnosticMode:
    startTime: UTCTime
    hint: str

    @staticmethod
    def _fromDict(obj):
        """
        Returns an ExecuteDiagnosticMode for the given dict.
        """
        startTime = UTCTime.from_str(obj['startTime'])
        hint = obj['hint']
        return ExecuteDiagnosticMode(startTime, hint)

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "startTime": str(self.startTime),
            "hint": self.hint
        }


class ExecuteOperationsMode:

    @staticmethod
    def _fromDict(_):
        return ExecuteOperationsMode()

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
        }

class GoOnline:

    @staticmethod
    def _fromDict(_):
        return GoOnline()

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
        }

class GoOffline:

    @staticmethod
    def _fromDict(_):
        return GoOffline()

    def _asDict(self):
        return {
            "_type": self.__class__.__name__,
        }
