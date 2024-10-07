from dataclasses import dataclass

from enum import Enum
from dataclasses import dataclass
from typing import Self

from csw.EnumUtil import UpperCaseEnum


class CalibrationLevel(Enum):
    Raw = 0
    Uncalibrated = 1
    Calibrated = 2
    ScienceProduct = 3
    AfterAnalysisScienceProduct = 4


@dataclass
class TYP:
    """
    Defines constants for the available subsystems
    """
    entryName: str
    description: str

    def longName(self) -> str:
        """
        Represents a string with entryName and description of a TYP
        """
        return f"{self.entryName} - {self.description}"

    def name(self) -> str:
        """
        Represents the name of the TYP e.g SCI
        """
        return self.entryName


class TYPs(UpperCaseEnum):
    SCI = TYP("SCI", "Science exposure")
    CAL = TYP("CAL", "Calibration exposure")
    ARC = TYP("ARC", "Wavelength calibration")
    IDP = TYP("IDP", "Instrumental dispersion")
    DRK = TYP("DRK", "Dark")
    MDK = TYP("MDK", "Master dark")
    FFD = TYP("FFD", "Flat field")
    NFF = TYP("NFF", "Normalized flat field")
    BIA = TYP("BIA", "Bias exposure")
    TEL = TYP("TEL", "Telluric standard")
    FLX = TYP("FLX", "Flux standard")
    SKY = TYP("SKY", "Sky background exposure")


@dataclass
class TYPLevel:
    typ: TYPs
    calibrationLevel: CalibrationLevel

    def __str__(self):
        return f"{self.typ.name}{self.calibrationLevel.value}"

    def calibrationLevelNumber(self) -> int:
        return self.calibrationLevel.value

    @classmethod
    def parseCalibrationLevel(cls, calibrationLevel: str) -> CalibrationLevel:
        try:
            return CalibrationLevel(int(calibrationLevel))
        except Exception as ex:
            raise ValueError(
                f"Failed to parse calibration level {calibrationLevel}: {repr(ex)}. Calibration level should be a digit.")

    @classmethod
    def make(cls, typLevel: str) -> Self:
        if not (len(typLevel) == 4):
            raise ValueError("requirement failed: TYPLevel must be a 3 character TYP followed by a calibration level")
        typ = typLevel[:3]
        calibrationLevel = typLevel[3:]
        level = cls.parseCalibrationLevel(calibrationLevel)
        return TYPLevel(TYPs.fromString(typ), level)
