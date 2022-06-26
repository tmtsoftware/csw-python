from dataclasses import dataclass
from typing import List

from csw.ControlCommand import ParameterSetType


@dataclass
class SequenceCommand(ParameterSetType):
    pass


@dataclass
class Wait(SequenceCommand):
    """
    A Wait command can only be sent to a sequencer
    """
    pass


@dataclass
class SequencerRequest:
    pass


@dataclass
class LoadSequence(SequencerRequest):
    sequence: List[SequenceCommand]
