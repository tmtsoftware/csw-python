from dataclasses import dataclass

from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from esw.ObsMode import ObsMode


class Variation:

    @classmethod
    def prefix(cls, subsystem: Subsystems, obsMode: ObsMode, variation: str | None = None) -> Prefix:
        if variation == None:
            return Prefix(subsystem, obsMode.name)
        return Prefix(subsystem, obsMode.name + "." + variation)
