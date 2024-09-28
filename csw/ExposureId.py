from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Self
from copy import deepcopy

from csw.ExposureNumber import ExposureNumber
from csw.ObsId import ObsId
from csw.Separator import Separator
from csw.Subsystem import Subsystem
from csw.TYPLevel import TYPLevel
from csw.UTCTime import UTCTime


@dataclass
class ExposureId:
    """
    ExposureId is an identifier in ESW/DMS for a single exposure.
    The ExposureId follows the structure: 2020A-001-123-WFOS-IMG1-SCI0-0001 with
    an included ObsId or when no ObsId is present, in the standalone
    format: 20200706-190204-WFOS-IMG1-SCI0-0001 with a UTC time when the
    ExposureId is created.

    obsId (ObsId | None): The (optional) Observation Id for the exposure.
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
    _exposureIdPattern = "%Y%m%dT%H%M%S"

    @classmethod
    def _formatDateTime(cls, utcTime: UTCTime):
        secs = utcTime.seconds + utcTime.nanos / 1e9
        dt = datetime.fromtimestamp(secs, timezone.utc)
        return dt.strftime(cls._exposureIdPattern)

    @classmethod
    def utcAsStandaloneString(cls, utcTime: UTCTime) -> str:
        return cls._formatDateTime(utcTime)

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

        XXXX TODO continue below ...


        #
        #   /**
        #    * A convenience function to create a new ExposureId with the next higher exposure number.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-123-WFOS-IMG1-SCI0-0002
        #    * @param exposureId current ExposureId
        #    * @return ExposureId with next higher exposure number
        #    */
        #   def nextExposureNumber(exposureId: ExposureId): ExposureId =
        #     updateExposureNumber(exposureId, exposureId.exposureNumber.next())
        #
        #   /**
        #    * A convenience function to create a new ExposureId with the same exposure number and
        #    * specified sub array number
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0001, 3 => 2020A-001-123-WFOS-IMG1-SCI0-0002-03.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0002-00, 4 => 2020A-001-123-WFOS-IMG1-SCI0-0002-04.
        #    * @param exposureId current ExposureId
        #    * @param subArrayNumber specified subArray number
        #    * @return ExposureId with next higher ExposureNumber
        #    */
        #   def withSubArrayNumber(exposureId: ExposureId, subArrayNumber: Int): ExposureId =
        #     updateExposureNumber(exposureId, ExposureNumber(exposureId.exposureNumber.exposureNumber, Some(subArrayNumber)))
        #
        #   /**
        #    * A convenience function to create a new ExposureId with the next higher sub array number.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-123-WFOS-IMG1-SCI0-0002-00.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0002-00 => 2020A-001-123-WFOS-IMG1-SCI0-0002-01.
        #    * @param exposureId current ExposureId
        #    * @return ExposureId with next higher ExposureNumber
        #    */
        #   def nextSubArrayNumber(exposureId: ExposureId): ExposureId =
        #     updateExposureNumber(exposureId, exposureId.exposureNumber.nextSubArray())
        #
        #   /**
        #    * A convenience function to create a new ExposureId with a new ObsId object.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-228-WFOS-IMG1-SCI0-0001.
        #    * Note that a standalone ExposureId will be changed to an ExposureId with an ObsId
        #    * @param exposureId current ExposureId
        #    * @param obsId new ObsId as an [[csw.params.core.models.ObsId]]
        #    * @return a new ExposureId with given new ObsId
        #    */
        #   def withObsId(exposureId: ExposureId, obsId: ObsId): ExposureId = {
        #     exposureId match {
        #       case expId: ExposureIdWithObsId =>
        #         expId.copy(obsId = Some(obsId))
        #       case _: StandaloneExposureId =>
        #         ExposureIdWithObsId(Some(obsId), exposureId.subsystem, exposureId.det, exposureId.typLevel, exposureId.exposureNumber)
        #     }
        #   }
        #
        #   /**
        #    * A convenience function to create a new ExposureId with a new ObsId as a String.
        #    * Example: 2020A-001-123-WFOS-IMG1-SCI0-0001 => 2020A-001-228-WFOS-IMG1-SCI0-0001.
        #    * Note that a standalone ExposureId will be changed to an ExposureId with an ObsId.
        #    * @param exposureId current ExposureId
        #    * @param obsIdString new ObsId as a String
        #    * @return ExposureId with given new [[csw.params.core.models.ObsId]]
        #    */
        #   def withObsId(exposureId: ExposureId, obsIdString: String): ExposureId =
        #     withObsId(exposureId, ObsId(obsIdString))
        #
        #   /**
        #    * A convenience function that allows creating a standalone ExposureId at a specific UTC date and time.
        #    * Note than an ExposureId with an ObsId can be changed to a standalone ExposureId.
        #    * @param exposureId current ExposureId
        #    * @param utc a [[csw.time.core.models.UTCTime]] for the ExposureId
        #    * @return a standalone ExposureId at the provided UTC
        #    */
        #   def withUTC(exposureId: ExposureId, utc: UTCTime): ExposureId =
        #     StandaloneExposureId(utc, exposureId.subsystem, exposureId.det, exposureId.typLevel, exposureId.exposureNumber)
        #
        #   /**
        #    * A helper function that allows creating exposure id from string in java file.
        #    * @param exposureId proper ExposureId as a String
        #    * @return instance of ExposureId
        #    */
        #   def fromString(exposureId: String): ExposureId = apply(exposureId)
        #
        #   /**
        #    * Create an ExposureId from a String of the 4 forms with and without an ObsId and with and without a subarray:
        #    * IRIS-IMG-SCI0-0001,IRIS-IMG-SCI0-0001-02 when no ObsId is present. Or
        #    * 2020A-001-123-IRIS-IMG-SCI0-0001 or 2020A-001-123-IRIS-IMG-SCI0-0001-02 when an ObsId is present.
        #    * @param exposureId proper ExposureId as a String
        #    * @return instance of ExposureId
        #    * @throws java.lang.IllegalArgumentException if the String does not follow the correct structure
        #    */
        #   def apply(exposureId: String): ExposureId = {
        #     val maxArgs: Int = 8
        #     exposureId.split(Separator.Hyphen, maxArgs) match {
        #       // 8 Args
        #       case Array(obs1, obs2, obs3, subsystemStr, detStr, typStr, expNumStr, subArrayStr) =>
        #         // This is the case with an ObsId and a sub array
        #         ExposureIdWithObsId(
        #           Some(ObsId(Separator.hyphenate(obs1, obs2, obs3))),
        #           Subsystem.withNameInsensitive(subsystemStr),
        #           detStr,
        #           TYPLevel(typStr),
        #           ExposureNumber(expNumStr + Separator.Hyphen + subArrayStr)
        #         )
        #       // 7 args
        #       case Array(p1, p2, p3, p4, p5, p6, p7) =>
        #         // This is the case with an ObsId and no subarray
        #         // Or Standalone with subarray
        #         // If it is with ObsId, the first part with be a semester ID which is always length 5
        #         if (p1.length == 5) {
        #           ExposureIdWithObsId(
        #             Some(ObsId(Separator.hyphenate(p1, p2, p3))),
        #             Subsystem.withNameInsensitive(p4),
        #             p5,
        #             TYPLevel(p6),
        #             ExposureNumber(p7)
        #           )
        #         }
        #         else {
        #           // It is a standalone with a subarray
        #           toTimeDateAtUTC(p1, p2) match {
        #             case Success(utcTime) =>
        #               StandaloneExposureId(
        #                 utcTime,
        #                 Subsystem.withNameInsensitive(p3),
        #                 p4,
        #                 TYPLevel(p5),
        #                 ExposureNumber(p6 + Separator.Hyphen + p7)
        #               )
        #             case Failure(ex) =>
        #               throw ex
        #           }
        #         }
        #       case Array(date, time, subsystemStr, detStr, typStr, expNumStr) if (date.length != 5) =>
        #         // 6 args - first two should be UTC time
        #         toTimeDateAtUTC(date, time) match {
        #           case Success(utcTime) =>
        #             StandaloneExposureId(
        #               utcTime,
        #               Subsystem.withNameInsensitive(subsystemStr),
        #               detStr,
        #               TYPLevel(typStr),
        #               ExposureNumber(expNumStr)
        #             )
        #           case Failure(ex) =>
        #             throw ex
        #         }
        #       case Array(subsystemStr, detStr, typStr, expNumStr, subArrayStr) =>
        #         // 5 args = this is standalone with subarray
        #         StandaloneExposureId(
        #           UTCTime.now(),
        #           Subsystem.withNameInsensitive(subsystemStr),
        #           detStr,
        #           TYPLevel(typStr),
        #           ExposureNumber(expNumStr + Separator.Hyphen + subArrayStr)
        #         )
        #       // 4 args
        #       case Array(subsystemStr, detStr, typStr, expNumStr) =>
        #         // This is standalone with no subarray
        #         StandaloneExposureId(
        #           UTCTime.now(),
        #           Subsystem.withNameInsensitive(subsystemStr),
        #           detStr,
        #           TYPLevel(typStr),
        #           ExposureNumber(expNumStr)
        #         )
        #       case _ =>
        #         throw new IllegalArgumentException(
        #           s"requirement failed: An ExposureId must be a ${Separator.Hyphen} separated string of the form " +
        #             "SemesterId-ProgramNumber-ObservationNumber-Subsystem-DET-TYPLevel-ExposureNumber"
        #         )
        #     }
        #   }
        #
        #   /** Convert an input date and time string to an Instant.  Throws parse exception on failure */
        #   private def toTimeDateAtUTC(dateStr: String, timeStr: String): Try[UTCTime] = Try {
        #     UTCTime(Instant.from(dateTimeFormatter.parse(s"$dateStr-$timeStr")))
        #   }
        #
        #   /**
        #    * This creates a stand-alone ExposureId for the case when there is no [[csw.params.core.models.ObsId]] available.
        #    * @param subsystem [[csw.prefix.models.Subsystem]] associated with exposure
        #    * @param det a valid detector String
        #    * @param typLevel the exposure's [[csw.params.core.models.TYPLevel]]
        #    * @param exposureNumber the exposure's Exposure Number [[csw.params.core.models.ExposureNumber]]
        #    * @return A stand-alone ExposureId
        #    */
        #   def apply(subsystem: Subsystem, det: String, typLevel: TYPLevel, exposureNumber: ExposureNumber): ExposureId =
        #     StandaloneExposureId(UTCTime.now(), subsystem: Subsystem, det: String, typLevel: TYPLevel, exposureNumber: ExposureNumber)
        #
        #   /**
        #    * This creates an ExposureId with an ObsId.
        #    * @param obsId a valid [[csw.params.core.models.ObsId]]
        #    * @param subsystem [[csw.prefix.models.Subsystem]] associated with exposure
        #    * @param det a valid detector String
        #    * @param typLevel the exposure's [[csw.params.core.models.TYPLevel]]
        #    * @param exposureNumber the exposure's Exposure Number [[csw.params.core.models.ExposureNumber]]
        #    * @return A standalone ExposureId
        #    */
        #   def apply(obsId: ObsId, subsystem: Subsystem, det: String, typLevel: TYPLevel, exposureNumber: ExposureNumber): ExposureId =
        #     ExposureIdWithObsId(Some(obsId), subsystem: Subsystem, det: String, typLevel: TYPLevel, exposureNumber: ExposureNumber)


@dataclass
class StandaloneExposureId(ExposureId):
    """
    A standalone ExposureId is an exposureId without an ObsId.
    Instances are created using the ExposureId object.
    """
    utcTime: UTCTime

    def __str__(self):
        t = ExposureId.utcAsStandaloneString(self.utcTime)
        return Separator.hyphenate(t, str(self.subsystem), str(self.det), str(self.typLevel), str(self.exposureNumber))

@dataclass
class ExposureIdWithObsId(ExposureId):
    """
     An ExposureIdWithObsId is an ExposureId with an included ObsId.
    Instances are created using the ExposureId object.
    """

    def __str__(self):
        return Separator.hyphenate(str(self.obsId), str(self.subsystem), str(self.det), str(self.typLevel), str(self.exposureNumber))

