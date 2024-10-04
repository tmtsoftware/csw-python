from dataclasses import dataclass

from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from esw.ObsMode import ObsMode


class Variation:

    @classmethod
    def prefix(cls, subsystem: Subsystem, obsMode: ObsMode, variation: str | None = None) -> Prefix:
        if variation == None:
            return Prefix(subsystem, obsMode.name)
        return Prefix(subsystem, obsMode.name + "." + variation)
