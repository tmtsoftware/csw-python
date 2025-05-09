from dataclasses import dataclass
from typing import Self

from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from esw.ObsMode import ObsMode

@dataclass
class Variation:
    name: str

    @classmethod
    def prefix(cls, subsystem: Subsystem, obsMode: ObsMode, variation: Self | None = None) -> Prefix:
        if variation is None:
            return Prefix(subsystem, obsMode.name)
        return Prefix(subsystem, obsMode.name + "." + variation.name)
