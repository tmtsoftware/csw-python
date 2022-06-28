from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from csw.ParameterSetType import SequenceCommand


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


class StartSequence(SequencerRequest):
    pass


class GetSequence(SequencerRequest):
    pass

# case class Add(commands: List[SequenceCommand])                 extends SequencerRequest
# case class Prepend(commands: List[SequenceCommand])             extends SequencerRequest
# case class Replace(id: Id, commands: List[SequenceCommand])     extends SequencerRequest
# case class InsertAfter(id: Id, commands: List[SequenceCommand]) extends SequencerRequest
# case class Delete(id: Id)                                       extends SequencerRequest
# case class AddBreakpoint(id: Id)                                extends SequencerRequest
# case class RemoveBreakpoint(id: Id)                             extends SequencerRequest
# case object Reset                                               extends SequencerRequest
# case object Pause                                               extends SequencerRequest
# case object Resume                                              extends SequencerRequest
# case object GetSequenceComponent                                extends SequencerRequest
# case object GetSequencerState                                   extends SequencerRequest
#
# case object IsAvailable   extends SequencerRequest
# case object IsOnline      extends SequencerRequest
# case object GoOnline      extends SequencerRequest
# case object GoOffline     extends SequencerRequest
# case object AbortSequence extends SequencerRequest
# case object Stop          extends SequencerRequest
#
# case class DiagnosticMode(startTime: UTCTime, hint: String) extends SequencerRequest
# case object OperationsMode                                  extends SequencerRequest
#
# // Sequencer Command Protocol
# case class Submit(sequence: Sequence) extends SequencerRequest
# case class Query(runId: Id)           extends SequencerRequest
