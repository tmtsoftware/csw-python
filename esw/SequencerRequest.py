from dataclasses import dataclass
from typing import List

from csw.ParameterSetType import SequenceCommand


@dataclass
class SequencerRequest:
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
        typ = obj["_type"]
        assert typ == 'LoadSequence'
        sequence = list(map(lambda p: SequenceCommand._fromDict(p), obj['sequence']))
        return LoadSequence(sequence)

