from dataclasses import dataclass
from typing import Self

from csw.ProgramId import ProgramId
from csw.Separator import Separator


@dataclass
class ObsId:
    """
    Represents a unique observation id

    programId (ProgramId): represents program Id
    observationNumber (int): Unique observation number in pattern O followed by 3-digit number
    """
    programId: ProgramId
    observationNumber: int

    def __post_init__(self):
        if not (self.observationNumber >= 1 and self.observationNumber <= 999):
            raise ValueError("requirement failed: Observation Number should be integer in the range of 1 to 999")

    def __str__(self):
        return Separator.hyphenate(f"{self.programId}", "{:03d}".format(self.observationNumber))

    @classmethod
    def make(cls, obsId: str) -> Self:
        match obsId.split(Separator.Hyphen):
            case [semesterId, programNumber, obsNumber] if obsNumber.isnumeric():
                return ObsId(ProgramId.make(Separator.hyphenate(semesterId, programNumber)), int(obsNumber))
            case _:
                raise ValueError(
                    f"{obsId}: An ObsId must consist of a semesterId, programNumber, and observationNumber separated by '{Separator.Hyphen}', ex: 2020A-001-123")
