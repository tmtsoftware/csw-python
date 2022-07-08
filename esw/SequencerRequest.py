from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from csw.ParameterSetType import SequenceCommand
from csw.UTCTime import UTCTime


@dataclass
class SequencerRequest:
    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
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
                return Delete.from_dict(obj)
            case 'Reset':
                return Reset()
            case 'Pause':
                return Pause()
            case 'Resume':
                return Resume()
            case 'AddBreakpoint':
                return AddBreakpoint.from_dict(obj)
            case 'RemoveBreakpoint':
                return RemoveBreakpoint.from_dict(obj)
            case 'AbortSequence':
                return AbortSequence()
            case 'Stop':
                return Stop()
            case 'Submit':
                return Submit._fromDict(obj)
            case 'Query':
                return Query.from_dict(obj)
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


@dataclass
class LoadSequence(SequencerRequest):
    sequence: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns a LoadSequence object for the given dict.
        """
        sequence = list(map(lambda p: SequenceCommand._fromDict(p), obj['sequence']))
        return LoadSequence(sequence)


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


@dataclass
class Replace(SequencerRequest):
    id_: str
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        id_ = obj['id']
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return Replace(id_, commands)


@dataclass
class InsertAfter(SequencerRequest):
    id_: str
    commands: List[SequenceCommand]

    # noinspection PyProtectedMember
    @staticmethod
    def _fromDict(obj):
        """
        Returns an Add object for the given dict.
        """
        id_ = obj['id']
        commands = list(map(lambda p: SequenceCommand._fromDict(p), obj['commands']))
        return InsertAfter(id_, commands)


@dataclass_json
@dataclass
class Delete(SequencerRequest):
    id: str


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


@dataclass_json
@dataclass
class RemoveBreakpoint(SequencerRequest):
    id: str


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

    @staticmethod
    def _fromDict(obj):
        """
        Returns a DiagnosticMode object for the given dict.
        """
        startTime = UTCTime.from_str(obj['startTime'])
        hint = obj['hint']
        return DiagnosticMode(startTime, hint)


class OperationsMode(SequencerRequest):
    pass


# Sequencer Command Protocol

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


@dataclass_json
@dataclass
class Query(SequencerRequest):
    runId: str
