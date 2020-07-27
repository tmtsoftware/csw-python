from dataclasses import dataclass
from typing import List

from csw.Parameter import Parameter


@dataclass
class CommandResponse:
    """
    Type of a response to a command (submit, oneway or validate).
    Note that oneway and validate responses are limited to Accepted, Invalid or Locked.
    """
    runId: str

    def _asDict(self):
        """
        Returns: XXX: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
        }


@dataclass
class Cancelled(CommandResponse):
    """Represents a negative response that describes the cancellation of command"""
    pass


@dataclass
class Accepted(CommandResponse):
    """Represents a final response stating acceptance of a command received"""
    pass


@dataclass
class Error(CommandResponse):
    """Represents a negative response that describes an error in executing the command"""
    message: str

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'message': self.message
        }


@dataclass
class Locked(CommandResponse):
    """Represents a negative response stating that a component is Locked and command was not validated or executed"""
    message: str

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'message': self.message
        }


@dataclass
class Started(CommandResponse):
    """Represents an intermediate response stating a long running command has been started"""
    message: str

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'message': self.message
        }


@dataclass
class Result:
    """A result containing parameters for command response"""
    paramSet: List[Parameter]

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }


@dataclass
class Completed(CommandResponse):
    """Represents a positive response stating completion of command"""
    result: Result = Result([])

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'result': self.result._asDict()
        }


# --- Invalid ---
@dataclass
class CommandIssue:
    """Describes a command issue with appropriate reason for validation failure"""
    reason: str


class HcdBusyIssue(CommandIssue):
    """Returned when the HCD is busy and can't process a command"""


class MissingKeyIssue(CommandIssue):
    """Returned when a command is missing a required key/parameter"""


class WrongPrefixIssue(CommandIssue):
    """Returned when an Assembly receives a configuration with a prefix that it doesn't support"""


class WrongParameterTypeIssue(CommandIssue):
    """Returned when the parameter for a key is not the correct type (i.e. int vs double, etc.)"""


class WrongUnitsIssue(CommandIssue):
    """Returned when a parameter value does not have the correct units"""


class WrongNumberOfParametersIssue(CommandIssue):
    """Returned when a command does not have the correct number of parameters"""


class AssemblyBusyIssue(CommandIssue):
    """Returned when an Assembly receives a command and one is already executing"""


class UnresolvedLocationsIssue(CommandIssue):
    """Returned when some required location is not available"""


class ParameterValueOutOfRangeIssue(CommandIssue):
    """Parameter of a command is out of range"""


class WrongInternalStateIssue(CommandIssue):
    """The component is in the wrong internal state to handle a command"""


class UnsupportedCommandInStateIssue(CommandIssue):
    """A command is unsupported in the current state"""


class UnsupportedCommandIssue(CommandIssue):
    """A command is unsupported by component"""


class RequiredServiceUnavailableIssue(CommandIssue):
    """A required service is not available"""


class RequiredHCDUnavailableIssue(CommandIssue):
    """A required HCD is not available"""


class RequiredAssemblyUnavailableIssue(CommandIssue):
    """A required Assembly is not available"""


class RequiredSequencerUnavailableIssue(CommandIssue):
    """Returned when some other issue occurred apart from those already defined"""


class OtherIssue(CommandIssue):
    """A required Sequencer is not available"""


@dataclass
class Invalid(CommandResponse):
    issue: CommandIssue

    def _asDict(self):
        """
        Returns: dict
            a dictionary for this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
            'issue': {
                "_type": self.issue.__class__.__name__,
                "reason": self.issue.reason
            }
        }
