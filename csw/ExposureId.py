from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Self
from copy import deepcopy

from csw.ExposureNumber import ExposureNumber
from csw.ObsId import ObsId
from csw.Separator import Separator
from csw.Subsystem import Subsystem
from csw.TYPLevel import TYPLevel
from csw.TMTTime import UTCTime


# noinspection SpellCheckingInspection
@dataclass
class ExposureId:
    """
    ExposureId is an identifier in ESW/DMS for a single exposure.
    The ExposureId follows the structure: 2020A-001-123-WFOS-IMG1-SCI0-0001 with
    an included ObsId or when no ObsId is present, in the standalone
    format: 20200706-190204-WFOS-IMG1-SCI0-0001 with a UTC time when the
    ExposureId is created.

    obsId (ObsId | None): The (optional) Observation ID for the exposure.
    subsystem (Subsystem): The Subsystem that produced the exposure
    det (str): The detector name associated with the exposure
    typLevel (TYPLevel): The exposure type and calibration level
    exposureNumber (ExposureNumber): The number of the exposure in a series.
    """
    obsId: ObsId | None
    subsystem: Subsystem
    det: str
    typLevel: TYPLevel
    exposureNumber: ExposureNumber

    # Used to format standalone ExposureId
    _exposureIdPattern = "%Y%m%d-%H%M%S"

    @classmethod
    def _formatDateTime(cls, utcTime: UTCTime) -> str:
        secs = utcTime.seconds + utcTime.nanos / 1e9
        dt = datetime.fromtimestamp(secs, timezone.utc)
        return dt.strftime(cls._exposureIdPattern)

    @classmethod
    def _parseDateTime(cls, timeStr: str) -> UTCTime:
        t = datetime.strptime(timeStr, cls._exposureIdPattern)
        epoch = datetime(1970, 1, 1)
        diff = (t - epoch).total_seconds()
        seconds = int(diff)
        nanos = int((diff - seconds) * 1e9)
        return UTCTime(seconds, nanos)

    @classmethod
    def updateExposureNumber(cls, exposureId: Self, update: ExposureNumber) -> Self:
        """
        Updates ExposureId with new ExposureNumber
        """
        copy = deepcopy(exposureId)
        copy.exposureNumber = update
        return copy

    @classmethod
    def withExposureNumber(cls, exposureId: Self, exposureNumber: int) -> Self:
        """
        A convenience function to create a new ExposureId with a specific exposure number.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 with 3 => 2020A-001-123-WFOS-IMG1-SCI0-0003

        Args:
            exposureId current ExposureId
            exposureNumber desired exposure number
        Returns
            ExposureId with specified exposure number
        """
        return cls.updateExposureNumber(exposureId, ExposureNumber(exposureNumber))

    @classmethod
    def nextExposureNumber(cls, exposureId: Self) -> Self:
        """
        A convenience function to create a new ExposureId with the next higher exposure number.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-123-WFOS-IMG1-SCI0-0002

        Args:
            exposureId current ExposureId

        Returns:
            ExposureId with next higher exposure number
        """
        return cls.updateExposureNumber(exposureId, exposureId.exposureNumber.next())

    @classmethod
    def withSubArrayNumber(cls, exposureId: Self, subArrayNumber: int) -> Self:
        """
        A convenience function to create a new ExposureId with the same exposure number and
        specified sub array number
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001, 3 => 2020A-001-123-WFOS-IMG1-SCI0-0002-03.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0002-00, 4 => 2020A-001-123-WFOS-IMG1-SCI0-0002-04.

        Args:
            exposureId: current ExposureId
            subArrayNumber: specified subArray number

        Returns:
            ExposureId with next higher ExposureNumber
        """
        return cls.updateExposureNumber(exposureId,
                                        ExposureNumber(exposureId.exposureNumber.exposureNumber, subArrayNumber))

    @classmethod
    def nextSubArrayNumber(cls, exposureId: Self) -> Self:
        """
        A convenience function to create a new ExposureId with the next higher sub array number.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-123-WFOS-IMG1-SCI0-0002-00.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0002-00 => 2020A-001-123-WFOS-IMG1-SCI0-0002-01.

        Args:
            exposureId: current ExposureId

        Returns:
            ExposureId with next higher sub array number
        """
        return cls.updateExposureNumber(exposureId, exposureId.exposureNumber.nextSubArray())

    @classmethod
    def withObsId(cls, exposureId: Self, obsId: ObsId) -> Self:
        """
        A convenience function to create a new ExposureId with a new ObsId object.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-228-WFOS-IMG1-SCI0-0001.
        Note that a standalone ExposureId will be changed to an ExposureId with an ObsId

        Args:
            exposureId: current ExposureId
            obsId: new ObsId

        Returns:
            a new ExposureId with given new ObsId
        """
        match exposureId:
            case ExposureIdWithObsId():
                copy = deepcopy(exposureId)
                copy.obsId = obsId
                return copy
            case _:
                return ExposureIdWithObsId(obsId, exposureId.subsystem, exposureId.det, exposureId.typLevel,
                                           exposureId.exposureNumber)

    @classmethod
    def withObsIdStr(cls, exposureId: Self, obsIdString: str) -> Self:
        """
        A convenience function to create a new ExposureId with a new ObsId as a string.
        Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-228-WFOS-IMG1-SCI0-0001.
        Note that a standalone ExposureId will be changed to an ExposureId with an ObsId

        Args:
            exposureId: current ExposureId
            obsIdString: new ObsId as a string

        Returns:
            a new ExposureId with given new ObsId
        """
        return cls.withObsId(exposureId, ObsId.make(obsIdString))

    @classmethod
    def withUTC(cls, exposureId: Self, utc: UTCTime) -> Self:
        """
        A convenience function that allows creating a standalone ExposureId at a specific UTC date and time.
        Note than an ExposureId with an ObsId can be changed to a standalone ExposureId.

        Args:
            exposureId: current ExposureId
            utc: a UTCTime for the ExposureId

        Returns:
            a standalone ExposureId at the provided UTC
        """
        return StandaloneExposureId(utcTime=utc, obsId=None, subsystem=exposureId.subsystem, det=exposureId.det,
                                    typLevel=exposureId.typLevel, exposureNumber=exposureId.exposureNumber)

    @classmethod
    def utcAsStandaloneString(cls, utcTime: UTCTime) -> str:
        return cls._formatDateTime(utcTime)

    @classmethod
    def fromString(cls, exposureId: str) -> Self:
        """
        A helper function that allows creating exposure id from string in java file.

        Returns:
            instance of ExposureId
        """
        return cls.make(exposureId)

    @classmethod
    def make(cls, exposureId: str) -> Self:
        """
        Create an ExposureId from a String of the 4 forms with and without an ObsId and with and without a subarray:
        IRIS-IMG-SCI0-0001,IRIS-IMG-SCI0-0001-02 when no ObsId is present. Or
        2020A-001-123-IRIS-IMG-SCI0-0001 or 2020A-001-123-IRIS-IMG-SCI0-0001-02 when an ObsId is present.

        Args:
            exposureId (str) proper ExposureId as a String:

        Returns:
            instance of ExposureId

        Raises ValueError if the String does not follow the correct structure
        """

        maxArgs = 8
        match exposureId.split(Separator.Hyphen, maxArgs):
            # 8 Args
            case [obs1, obs2, obs3, subsystemStr, detStr, typStr, expNumStr, subArrayStr]:
                # This is the case with an ObsId and a sub array
                return ExposureIdWithObsId(
                    obsId=ObsId.make(Separator.hyphenate(obs1, obs2, obs3)),
                    subsystem=Subsystem.fromString(subsystemStr),
                    det=detStr,
                    typLevel=TYPLevel.make(typStr),
                    exposureNumber=ExposureNumber.make(f"{expNumStr}{Separator.Hyphen}{subArrayStr}"))

            # 7 args
            case [p1, p2, p3, p4, p5, p6, p7]:
                # This is the case with an ObsId and no subarray
                # Or Standalone with subarray
                # If it is with ObsId, the first part with be a semester ID which is always length 5
                if len(p1) == 5:
                    return ExposureIdWithObsId(
                        obsId=ObsId.make(Separator.hyphenate(p1, p2, p3)),
                        subsystem=Subsystem.fromString(p4),
                        det=p5,
                        typLevel=TYPLevel.make(p6),
                        exposureNumber=ExposureNumber.make(p7))
                else:
                    # It is a standalone with a subarray
                    return StandaloneExposureId(
                        obsId=None,
                        subsystem=Subsystem.fromString(p3),
                        det=p4,
                        typLevel=TYPLevel.make(p5),
                        exposureNumber=ExposureNumber.make(f"{p6}{Separator.Hyphen}{p7}"),
                        utcTime=cls.toTimeDateAtUTC(p1, p2))

            case [date, time, subsystemStr, detStr, typStr, expNumStr] if (len(date) != 5):
                # 6 args - first two should be UTC time
                return StandaloneExposureId(
                    obsId=None,
                    subsystem=Subsystem.fromString(subsystemStr),
                    det=detStr,
                    typLevel=TYPLevel.make(typStr),
                    exposureNumber=ExposureNumber.make(expNumStr),
                    utcTime=cls.toTimeDateAtUTC(date, time))

            case [subsystemStr, detStr, typStr, expNumStr, subArrayStr]:
                # 5 args = this is standalone with subarray
                return StandaloneExposureId(
                    obsId=None,
                    subsystem=Subsystem.fromString(subsystemStr),
                    det=detStr,
                    typLevel=TYPLevel.make(typStr),
                    exposureNumber=ExposureNumber.make(f"{expNumStr}{Separator.Hyphen}{subArrayStr}"),
                    utcTime=UTCTime.now())
            # 4 args
            case [subsystemStr, detStr, typStr, expNumStr]:
                # This is standalone with no subarray
                return StandaloneExposureId(
                    obsId=None,
                    subsystem=Subsystem.fromString(subsystemStr),
                    det=detStr,
                    typLevel=TYPLevel.make(typStr),
                    exposureNumber=ExposureNumber.make(expNumStr),
                    utcTime=UTCTime.now(),
                )
            case _:
                raise ValueError(
                    f"requirement failed: An ExposureId must be a {Separator.Hyphen} separated string of the form " +
                    "SemesterId-ProgramNumber-ObservationNumber-Subsystem-DET-TYPLevel-ExposureNumber"
                )

    @classmethod
    def toTimeDateAtUTC(cls, dateStr: str, timeStr: str) -> UTCTime:
        """
        Convert an input date and time string to an Instant.  Throws parse exception on failure
        """
        return cls._parseDateTime(f"{dateStr}-{timeStr}")

    @classmethod
    def makeStandalone(cls, subsystem: Subsystem, det: str, typLevel: TYPLevel, exposureNumber: ExposureNumber) -> Self:
        """
        This creates a stand-alone ExposureId for the case when there is no ObsId available
        Args:
            subsystem (Subsystem): associated with exposure
            det (str): a valid detector String
            typLevel (TYPLevel): the exposure's TYPLevel
            exposureNumber (ExposureNumber) the exposure's Exposure Number:

        Returns:
            A stand-alone ExposureId
        """
        return StandaloneExposureId(
            obsId=None,
            utcTime=UTCTime.now(),
            subsystem=subsystem,
            det=det,
            typLevel=typLevel,
            exposureNumber=exposureNumber)

    @classmethod
    def makeWithObsId(cls, obsId: ObsId, subsystem: Subsystem, det: str, typLevel: TYPLevel,
                      exposureNumber: ExposureNumber) -> Self:
        """
        This creates an ExposureId with an ObsId
        Args:
            obsId (ObsId): a valid ObsId
            subsystem (Subsystem): associated with exposure
            det (str): a valid detector String
            typLevel (TYPLevel): the exposure's TYPLevel
            exposureNumber (ExposureNumber) the exposure's Exposure Number:

        Returns:
            A stand-alone ExposureId
        """
        return StandaloneExposureId(
            obsId=obsId,
            utcTime=UTCTime.now(),
            subsystem=subsystem,
            det=det,
            typLevel=typLevel,
            exposureNumber=exposureNumber)


@dataclass
class StandaloneExposureId(ExposureId):
    """
    A standalone ExposureId is an exposureId without an ObsId.
    Instances are created using the ExposureId object.
    """
    utcTime: UTCTime

    def __str__(self):
        t = ExposureId.utcAsStandaloneString(self.utcTime)
        return Separator.hyphenate(t, self.subsystem.name, str(self.det), str(self.typLevel), str(self.exposureNumber))


@dataclass
class ExposureIdWithObsId(ExposureId):
    """
     An ExposureIdWithObsId is an ExposureId with an included ObsId.
    Instances are created using the ExposureId object.
    """

    def __str__(self):
        return Separator.hyphenate(str(self.obsId), self.subsystem.name, str(self.det), str(self.typLevel),
                                   str(self.exposureNumber))
