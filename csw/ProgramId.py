from dataclasses import dataclass
from typing import Self

from csw.SemesterId import SemesterId
from csw.Separator import Separator


@dataclass
class ProgramId:
    """
    Represents a unique program id

    semesterId (SemesterId): semesterId for Program
    programNumber (int): programNumber number in pattern P followed by 3-digit number
    """

    semesterId: SemesterId
    programNumber: int

    def __post_init__(self):
        if not (self.programNumber >= 1 and self.programNumber <= 999):
            raise ValueError("requirement failed: Program Number should be integer in the range of 1 to 999")

    def __str__(self):
        return Separator.hyphenate(f"{self.semesterId}", "{:03d}".format(self.programNumber))

    @classmethod
    def make(cls, programId: str) -> Self:
        match programId.split(Separator.Hyphen):
            case [semesterId, programNumber] if programNumber.isnumeric():
                return ProgramId(SemesterId.make(semesterId), int(programNumber))
            case _:
                raise ValueError(
                    f"A program Id consists of a semester Id and program number separated by '{Separator.Hyphen}', ex: 2020A-001")
