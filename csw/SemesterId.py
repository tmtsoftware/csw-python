from dataclasses import dataclass
from enum import Enum
from typing import Self


class Semester(Enum):
    A = 1
    B = 2


@dataclass
class SemesterId:
    """
    Represents a unique semester id

    Args:
        year (int): year for semester
        semester (Semester): observing semester
    """
    year: int
    semester: Semester

    def __str__(self):
        return f"{self.year}{self.semester.name}"

    @staticmethod
    def _parseSemester(semesterStr: str) -> Semester:
        if not semesterStr in Semester.__members__:
            semesters = ", ".join(Semester.__members__.keys())
            raise ValueError(
                f"Failed to parse semester {semesterStr}: {semesterStr} is not a member of Enum ({semesters})")
        return Semester[semesterStr]

    @classmethod
    def make(cls, semesterId: str) -> Self:
        n = len(semesterId) - 1
        yearStr, semesterStr = semesterId[:n], semesterId[n:]
        if not (yearStr.isnumeric()):
            raise ValueError(f"{yearStr} should be valid year")
        year = int(yearStr)
        semester = cls._parseSemester(semesterStr)
        return SemesterId(year, semester)
