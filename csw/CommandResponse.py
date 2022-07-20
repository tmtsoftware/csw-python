from dataclasses import dataclass
from typing import List

from csw.Parameter import Parameter


# noinspection PyProtectedMember
@dataclass
class CommandResponse:
    """
    Type of a response to a command (submit, oneway or validate).
    Note that oneway and validate responses are limited to Accepted, Invalid or Locked.
    """
    runId: str

    def _asDict(self):
        """
        Returns: a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
        }

    @staticmethod
    def _fromDict(obj: dict):
        match obj["_type"]:
            case "Cancelled":
                return Cancelled._fromDict(obj)
            case "Error":
                return Error._fromDict(obj)
            case "Locked":
                return Locked._fromDict(obj)
            case "Started":
                return Started._fromDict(obj)
            case "Completed":
                return Completed._fromDict(obj)
            case "Accepted":
                return Accepted._fromDict(obj)
            case "Invalid":
                return Invalid._fromDict(obj)


@dataclass
class Cancelled(CommandResponse):
    """Represents a negative response that describes the cancellation of command"""

    @staticmethod
    def _fromDict(obj: dict):
        return Cancelled(
            runId=obj['runId']
        )


@dataclass
class Accepted(CommandResponse):
    """Represents a final response stating acceptance of a command received"""

    @staticmethod
    def _fromDict(obj: dict):
        return Accepted(
            runId=obj['runId']
        )


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

    @staticmethod
    def _fromDict(obj: dict):
        return Error(
            runId=obj['runId'],
            message=obj['message']
        )


@dataclass
class Locked(CommandResponse):
    """Represents a negative response stating that a component is Locked and command was not validated or executed"""

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
        }

    @staticmethod
    def _fromDict(obj: dict):
        return Locked(
            runId=obj['runId'],
        )


@dataclass
class Started(CommandResponse):
    """Represents an intermediate response stating a long-running command has been started"""

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'runId': self.runId,
        }

    @staticmethod
    def _fromDict(obj: dict):
        return Started(
            runId=obj['runId'],
        )


@dataclass
class Result:
    """A result containing parameters for command response"""
    paramSet: List[Parameter]

    # noinspection PyProtectedMember
    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a Result for the given dict.
        """
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        return Result(paramSet)


@dataclass
class Completed(CommandResponse):
    """Represents a positive response stating completion of command"""
    result: Result = Result([])

    # noinspection PyProtectedMember
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

    @staticmethod
    def _fromDict(obj: dict):
        return Completed(
            runId=obj['runId'],
            result=Result._fromDict(obj['result']),
        )


# --- Invalid ---
@dataclass
class CommandIssue:
    """Describes a command issue with appropriate reason for validation failure"""
    reason: str

    @staticmethod
    def _fromDict(obj: dict):
        return globals()[obj['_type']](obj['reason'])


class IdNotAvailableIssue(CommandIssue):
    """Returned when a CommandResponse associated with runId is not available"""


class HCDBusyIssue(CommandIssue):
    """Returned when the HCD is busy and can't process a command"""


class WrongCommandTypeIssue(CommandIssue):
    """Returned when the given command type is not expected"""


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

    @staticmethod
    def _fromDict(obj: dict):
        return Invalid(
            runId=obj['runId'],
            issue=CommandIssue._fromDict(obj['issue']),
        )


SubmitResponse = Error | Invalid | Locked | Started | Completed | Cancelled
ValidateResponse = Accepted | Invalid | Locked
OnewayResponse = Accepted | Invalid | Locked
