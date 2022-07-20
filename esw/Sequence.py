from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from csw.ParameterSetType import SequenceCommand

@dataclass_json
@dataclass
class Sequence:
    commands: List[SequenceCommand]
