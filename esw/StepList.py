from dataclasses import dataclass
from typing import List

from esw.Step import Step


@dataclass
class StepList:
    steps: List[Step]

    @staticmethod
    def _fromDict(obj):
        """
        Returns a LoadSequence object for the given dict.
        """
        if (len(obj) != 0):
            steps = list(map(lambda p: Step._fromDict(p), obj[0]))
            return StepList(steps)
        return None
