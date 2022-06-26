from dataclasses import dataclass
from typing import List

from csw.ParameterSetType import SequenceCommand


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
                pass
            case 'Add':
                pass
            case 'Prepend':
                pass
            case 'Replace':
                pass
            case 'InsertAfter':
                pass
            case 'Delete':
                pass
            case 'Pause':
                pass
            case 'Resume':
                pass
            case 'AddBreakpoint':
                pass
            case 'RemoveBreakpoint':
                pass
            case 'Reset':
                pass
            case 'AbortSequence':
                pass
            case 'Stop':
                pass
            case 'Submit':
                pass
            case 'Query':
                pass
            case 'GoOnline':
                pass
            case 'GoOffline':
                pass
            case 'DiagnosticMode':
                pass
            case 'OperationsMode':
                pass
            case 'GetSequenceComponent':
                pass
            case 'GetSequencerState':
                pass


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


@dataclass
class StartSequence(SequencerRequest):
    pass
