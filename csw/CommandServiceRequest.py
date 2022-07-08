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
_pdocIgnoreGenerated("Submit")
_pdocIgnoreGenerated("Oneway")
_pdocIgnoreGenerated("QueryFinal")
_pdocIgnoreGenerated("SubscribeCurrentState")


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
