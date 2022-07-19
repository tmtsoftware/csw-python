from dataclasses import dataclass
from typing import List

from esw.Step import Step


@dataclass
class StepList:
    steps: List[Step]
