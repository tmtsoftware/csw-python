from dataclasses import dataclass
from typing import List, Self

from dataclasses_json import dataclass_json

from csw.ParameterSetType import SequenceCommand
from csw.TMTTime import UTCTime


# noinspection PyProtectedMember

@dataclass
class SequencerRequest:

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
        }

    # noinspection PyProtectedMember
    @classmethod
    def _fromDict(cls, obj) -> Self:
        """
        Returns a LoadSequence object for the given dict.
        """
        method = obj['_type']
        match method:
            case 'LoadSequence':
                return LoadSequence._fromDict(obj)
            case 'StartSequence':
                return StartSequence()
            case 'GetSequence':
                return GetSequence()
            case 'Add':
                return Add._fromDict(obj)
            case 'Prepend':
                return Prepend._fromDict(obj)
            case 'Replace':
                return Replace._fromDict(obj)
            case 'InsertAfter':
                return InsertAfter._fromDict(obj)
            case 'Delete':
                return Delete._fromDict(obj)
            case 'Reset':
                return Reset()
            case 'Pause':
                return Pause()
            case 'Resume':
                return Resume()
            case 'AddBreakpoint':
                return AddBreakpoint._fromDict(obj)
            case 'RemoveBreakpoint':
                return RemoveBreakpoint._fromDict(obj)
            case 'AbortSequence':
                return AbortSequence()
            case 'Stop':
                return Stop()
            case 'Submit':
                return Submit._fromDict(obj)
            case 'Query':
                return Query._fromDict(obj)
            case 'GoOnline':
                return GoOnline()
            case 'GoOffline':
                return GoOffline()
            case 'DiagnosticMode':
                return DiagnosticMode._fromDict(obj)
            case 'OperationsMode':
                return OperationsMode()
            case 'GetSequenceComponent':
                return GetSequenceComponent()
            case 'GetSequencerState':
                return GetSequencerState()
            # -- For scripts ----------
            case 'PullNext':
                return PullNext()
            case 'MaybeNext':
                return MaybeNext()
            case 'ReadyToExecuteNext':
                return ReadyToExecuteNext()
            case 'StepSuccess':
                return StepSuccess()
            case 'StepFailure':
                return StepFailure._fromDict(obj)
        # --------------------------------


# noinspection DuplicatedCode,PyProtectedMember
@dataclass
class LoadSequence(SequencerRequest):
    sequence: List[SequenceCommand]

    @classmethod
    def _fromDict(cls, obj) ->Self:
        """
        Returns a LoadSequence object for the given dict.
        """
        sequence = list(map(lambda p: SequenceCommand._fromDict(p), obj['sequence']))
        return cls(sequence)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "sequence": list(map(lambda p: p._asDict(), self.sequence))
        }


class StartSequence(SequencerRequest):
    pass


class GetSequence(SequencerRequest):
    pass


@dataclass
class Add(SequencerRequest):
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return Add(commands)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "commands": list(map(lambda p: p._asDict(), self.commands))
        }


@dataclass
class Prepend(SequencerRequest):
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return Prepend(commands)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "commands": list(map(lambda p: p._asDict(), self.commands))
        }


@dataclass
class Replace(SequencerRequest):
    id: str
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        id = obj['id']
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return Replace(id, commands)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "id": self.id,
            "commands": list(map(lambda p: p._asDict(), self.commands))
        }


@dataclass
class InsertAfter(SequencerRequest):
    id: str
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        id = obj['id']
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return InsertAfter(id, commands)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "id": self.id,
            "commands": list(map(lambda p: p._asDict(), self.commands))
        }


@dataclass
class Delete(SequencerRequest):
    id: str

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        id = obj['id']
        return Delete(id)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "id": self.id
        }


class Reset(SequencerRequest):
    pass


class Pause(SequencerRequest):
    pass


class Resume(SequencerRequest):
    pass


@dataclass_json
@dataclass
class AddBreakpoint(SequencerRequest):
    id: str

    # noinspection PyProtectedMember
    @classmethod
    def _fromDict(cls, obj) -> Self:
        """
        Returns an Add object for the given dict.
        """
        id = obj['id']
        return cls(id)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "id": self.id
        }


@dataclass_json
@dataclass
class RemoveBreakpoint(SequencerRequest):
    id: str

    # noinspection PyProtectedMember
    @classmethod
    def _fromDict(cls, obj) -> Self:
        """
        Returns an Add object for the given dict.
        """
        id = obj['id']
        return cls(id)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "id": self.id
        }


class GetSequenceComponent(SequencerRequest):
    pass


class GetSequencerState(SequencerRequest):
    pass


class IsAvailable(SequencerRequest):
    pass


class IsOnline(SequencerRequest):
    pass


class GoOnline(SequencerRequest):
    pass


class GoOffline(SequencerRequest):
    pass


class AbortSequence(SequencerRequest):
    pass


class Stop(SequencerRequest):
    pass


@dataclass
class DiagnosticMode(SequencerRequest):
    startTime: UTCTime
    hint: str

    @classmethod
    def _fromDict(cls, obj) -> Self:
        """
        Returns a DiagnosticMode object for the given dict.
        """
        startTime = UTCTime.from_str(obj['startTime']['value'])
        hint = obj['hint']
        return cls(startTime, hint)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "startTime": str(self.startTime),
            "hint": self.hint,
        }


class OperationsMode(SequencerRequest):
    pass


# -- For scripts --

class PullNext(SequencerRequest):
    pass


class MaybeNext(SequencerRequest):
    pass


class ReadyToExecuteNext(SequencerRequest):
    pass


class StepSuccess(SequencerRequest):
    pass


@dataclass
class StepFailure(SequencerRequest):
    message: str

    @classmethod
    def _fromDict(cls, obj) -> Self:
        message = obj['message']
        return cls(message)


# -- Sequencer Command Protocol --

@dataclass
class Submit(SequencerRequest):
    sequence: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a Submit object for the given dict.
        """
        sequence = list(map(lambda p: SequenceCommand._fromDict(p), obj['sequence']))
        return LoadSequence(sequence)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "sequence": list(map(lambda p: p._asDict(), self.sequence))
        }


@dataclass
class Query(SequencerRequest):
    runId: str

    # noinspection PyProtectedMember
    @classmethod
    def _fromDict(cls, obj) -> Self:
        """
        Returns an Add object for the given dict.
        """
        runId = obj['runId']
        return cls(runId)

    def _asDict(self) -> dict:
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            "runId": self.runId
        }
