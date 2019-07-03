from dataclasses import dataclass
from typing import List

from csw.Parameter import Parameter


@dataclass
class SubmitResponse:
    """
    SubmitResponse is returned by Submit message which calls the onSubmit handler
    Responses returned can be Invalid, Started, Completed, CompletedWithResult, Error, Cancelled, Locked
    """
    runId: str

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {
            'runId': self.runId,
        }


@dataclass
class Completed(SubmitResponse):
    """Represents a positive response stating completion of command"""
    pass


@dataclass
class Cancelled(SubmitResponse):
    """Represents a negative response that describes the cancellation of command"""
    pass


@dataclass
class Error(SubmitResponse):
    """Represents a negative response that describes an error in executing the command"""
    message: str

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {
            'runId': self.runId,
            'message': self.message
        }

@dataclass
class Locked(SubmitResponse):
    """Represents a negative response stating that a component is Locked and command was not validated or executed"""
    message: str


@dataclass
class Started(SubmitResponse):
    """Represents an intermediate response stating a long running command has been started"""
    message: str


# --- CompletedWithResult ---
@dataclass
class Result:
    """A result containing parameters for command response"""
    prefix: str
    paramSet: List[Parameter]

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {
            'prefix': self.prefix,
            'paramSet': list(map(lambda p: p.asDict(), self.paramSet))
        }


# """
# {
#   "CompletedWithResult": {
#     "runId": "0e537918-7272-4e10-b20f-82861d084873",
#     "result": {
#       "prefix": "wfos.prog.cloudcover",
#       "paramSet": [
#         {
#           "keyName": "encoder",
#           "keyType": "IntKey",
#           "items": [
#             20
#           ],
#           "units": "NoUnits"
#         }
#       ]
#     }
#   }
# }
#
# """


@dataclass
class CompletedWithResult(SubmitResponse):
    """Represents a positive response stating completion of command"""
    result: Result

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {
            'runId': self.runId,
            'result': self.result.asDict()
        }


# ---

# --- Invalid ---
@dataclass
class CommandIssue:
    """Describes a command issue with appropriate reason for validation failure"""
    reason: str


@dataclass
class MissingKeyIssue(CommandIssue):
    """Returned when a command is missing a required key/parameter"""


class WrongPrefixIssue(CommandIssue):
    """Returned when an Assembly receives a configuration with a Prefix that it doesn't support"""


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


# """
# {
#   "Invalid": {
#     "runId": "7af2722e-3a92-4522-b7da-b1d063ddaf67",
#     "issue": {
#       "OtherIssue": {
#         "reason": "test issue"
#       }
#     }
#   }
# }
#
# """


@dataclass
class Invalid(SubmitResponse):
    issue: CommandIssue

    def asDict(self):
        """
        :return: dictionary to be encoded to CBOR
        """
        return {
            'runId': self.runId,
            'issue': {
                str(self.issue.__class__.__name__): {
                    "reason": self.issue.reason
                }
            }
        }

# ---
