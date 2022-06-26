import traceback
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from csw.ParameterSetType import ControlCommand

# Ignore generated functions in API docs
__pdoc__ = {}

def _pdocIgnoreGenerated(className: str):
    __pdoc__[f"{className}.from_dict"] = False
    __pdoc__[f"{className}.from_json"] = False
    __pdoc__[f"{className}.schema"] = False
    __pdoc__[f"{className}.to_dict"] = False
    __pdoc__[f"{className}.to_json"] = False


_pdocIgnoreGenerated("Validate")


@dataclass_json
@dataclass
class Validate:
    """
    A message sent to validate a command. The response should be one of: Accepted, Invalid or Locked.

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("Submit")


@dataclass_json
@dataclass
class Submit:
    """
    Represents a command that requires a response (of type CommandResponse).

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("Oneway")


@dataclass_json
@dataclass
class Oneway:
    """
    Represents a command that does not require or expect a response

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("QueryFinal")


@dataclass_json
@dataclass
class QueryFinal:
    """
    A message sent to query the final result of a long running command.
    The response should be a CommandResponse.

    Args:
        runId (str): The command's runId
        timeoutInSeconds (int) amount of time to wait
    """
    runId: str
    timeoutInSeconds: int

    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        try:
            runId = obj['runId']
            timeoutInSeconds = obj['timeoutInSeconds']
            return QueryFinal(runId, timeoutInSeconds)
        except:
            traceback.print_exc()


_pdocIgnoreGenerated("SubscribeCurrentState")


@dataclass_json
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
        # typ = obj["_type"]
        if "names" in obj.keys():
            stateNames = obj.get("names")
        else:
            stateNames = []
        return SubscribeCurrentState(stateNames)
