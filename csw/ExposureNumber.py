from dataclasses import dataclass
from typing import Self

from csw.Separator import Separator


@dataclass
class ExposureNumber:
    exposureNumber: int
    subArray: int | None = None

    def __str__(self):
        if (self.subArray is None):
            return f"{self.exposureNumber:04d}"
        else:
            return f"{self.exposureNumber:04d}-{self.subArray:02d}"

    def next(self) -> Self:
        """
        Returns the next exposure number
        """
        return ExposureNumber(self.exposureNumber + 1, self.subArray)

    def nextSubArray(self) -> Self:
        """
        Returns the next subarray number
        """
        if (self.subArray is None):
            return ExposureNumber(self.exposureNumber, 0)
        else:
            return ExposureNumber(self.exposureNumber, self.subArray + 1)

    @classmethod
    def default(cls) -> Self:
        """
        A convenience to use when constructing ExposureId
        """
        return cls(0)

    @staticmethod
    def _parseToInt(exposureNo: str, allowedLength: int) -> int:
        if not (len(exposureNo) == allowedLength and exposureNo.isnumeric()):
            raise ValueError(
                f"requirement failed: Invalid exposure number: {exposureNo}. An ExposureNumber must be a 4 digit number and optional 2 digit sub array in format XXXX or XXXX-XX")
        return int(exposureNo)

    @classmethod
    def make(cls, exposureNumber: str) -> Self:
        match exposureNumber.split(Separator.Hyphen):
            case [exposureArrayStr, exposureNoSubArrayStr]:
                exposureArray = cls._parseToInt(exposureArrayStr, allowedLength=4)
                subArray = cls._parseToInt(exposureNoSubArrayStr, allowedLength=2)
                return ExposureNumber(exposureArray, subArray)
            case [exposureArrayStr]:
                return ExposureNumber(cls._parseToInt(exposureArrayStr, allowedLength=4))
            case _:
                raise ValueError()
