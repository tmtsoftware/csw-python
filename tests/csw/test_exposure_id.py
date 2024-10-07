import pytest

from csw.ExposureId import ExposureId, ExposureIdWithObsId, StandaloneExposureId
from csw.ExposureNumber import ExposureNumber
from csw.ObsId import ObsId
from csw.Subsystem import Subsystem
from csw.TYPLevel import TYPLevel
from csw.UTCTime import UTCTime


# create ExposureId from String and validate members

def test_1():
    """
    should create valid ExposureId with ObsId | CSW-121
    """
    exposureId = ExposureId.make("2020A-001-123-CSW-IMG1-SCI0-0001")
    # Verify parts
    assert (str(exposureId) == "2020A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.obsId == ObsId.make("2020A-001-123"))
    assert (exposureId.det == "IMG1")
    assert (exposureId.subsystem == Subsystem.CSW)
    assert (exposureId.typLevel == TYPLevel.make("SCI0"))
    assert (exposureId.exposureNumber == ExposureNumber.make("0001"))
    # verify total equality once
    assert (exposureId == ExposureIdWithObsId(ObsId.make("2020A-001-123"), Subsystem.CSW, "IMG1",
                                              TYPLevel.make("SCI0"), ExposureNumber.make("0001")))


def test_utc_time():
    utcTime = UTCTime.now()
    s = str(utcTime)
    x = UTCTime.from_str(s)
    assert (s == str(x))


def test_2():
    """
    should create valid ExposureId from a String with no ObsId | CSW-121
    """
    # For testing only to get at UTC for equality test below
    utcTime = UTCTime.now()
    exposureId = ExposureId.withUTC(ExposureId.make("CSW-IMG1-SCI0-0001"), utcTime)

    # noinspection PyTypeChecker
    standaloneExpId: StandaloneExposureId = exposureId
    assert (str(exposureId) == f"{ExposureId.utcAsStandaloneString(utcTime)}-CSW-IMG1-SCI0-0001")

    # Verify parts are correct once for standalone
    assert (exposureId.obsId is None)
    assert (exposureId.det == "IMG1")
    assert (exposureId.subsystem == Subsystem.CSW)
    assert (exposureId.typLevel == TYPLevel.make("SCI0"))
    assert (exposureId.exposureNumber == ExposureNumber.make("0001"))
    # verify total equality once
    assert (exposureId == StandaloneExposureId(None, Subsystem.CSW, "IMG1", TYPLevel.make("SCI0"),
                                               ExposureNumber.make("0001"), standaloneExpId.utcTime))


def test_3():
    """
    should create valid ExposureId from a String with and without ObsId or subArray | CSW-121
    """
    exposureId = ExposureId.make("2031A-001-123-CSW-IMG1-SCI0-0001-00")
    assert (str(exposureId) == "2031A-001-123-CSW-IMG1-SCI0-0001-00")
    assert (exposureId.exposureNumber.exposureNumber == 1)
    assert (exposureId.exposureNumber.subArray == 0)

    exposureId2 = ExposureId.make("2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (str(exposureId2) == "2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId2.exposureNumber.exposureNumber == 1)
    assert (exposureId2.exposureNumber.subArray is None)

    testUTC = UTCTime.now()
    exposureId3 = ExposureId.withUTC(ExposureId.make("CSW-IMG1-SCI0-0001"), testUTC)
    assert (str(exposureId3) == f"{ExposureId.utcAsStandaloneString(testUTC)}-CSW-IMG1-SCI0-0001")
    assert (exposureId3.exposureNumber.exposureNumber == 1)
    assert (exposureId3.exposureNumber.subArray is None)

    exposureId4 = ExposureId.withUTC(ExposureId.make("CSW-IMG1-SCI0-0001-04"), testUTC)
    assert (str(exposureId4) == f"{ExposureId.utcAsStandaloneString(testUTC)}-CSW-IMG1-SCI0-0001-04")
    assert (exposureId4.exposureNumber.exposureNumber == 1)
    assert (exposureId4.exposureNumber.subArray == 4)

    # Should be able to parse a standalone with and without subArray
    testStandalone = "20210806-005937-CSW-IMG1-SCI0-0001"
    exposureId5 = ExposureId.make(testStandalone)
    assert (exposureId5.exposureNumber.exposureNumber == 1)
    assert (str(exposureId5) == testStandalone)

    testStandalone2 = "20210806-005937-CSW-IMG1-SCI0-0002-03"
    exposureId6 = ExposureId.make(testStandalone2)
    assert (exposureId6.exposureNumber.exposureNumber == 2)
    assert (exposureId6.exposureNumber.subArray == 3)
    assert (str(exposureId6) == testStandalone2)


def test_4():
    """
    should create valid ExposureId with no ObsId and then add ObsId | CSW-121
    """
    exposureId = ExposureId.make("CSW-IMG1-SCI0-0001")
    assert (exposureId.obsId is None)

    exposureIdWithObsId = ExposureId.withObsId(exposureId, ObsId.make("2020B-100-456"))
    # verify total equality
    assert (exposureIdWithObsId == ExposureIdWithObsId(ObsId.make("2020B-100-456"), Subsystem.CSW, "IMG1",
                                                       TYPLevel.make("SCI0"), ExposureNumber.make("0001")))
    obsId = ObsId.make("2021B-200-007")
    exposureIdWithObsId2 = ExposureId.withObsId(exposureId, obsId)
    assert (exposureIdWithObsId2 == ExposureIdWithObsId(ObsId.make("2021B-200-007"), Subsystem.CSW, "IMG1",
                                                        TYPLevel.make("SCI0"), ExposureNumber.make("0001")))


def test_5():
    """
    should throw exception if invalid obsId in exposure Id | CSW-121
    """
    with pytest.raises(ValueError,
                       match="A program Id consists of a semester Id and program number separated by '-', ex: 2020A-001"):
        ExposureId.make("2020A-ABC-123-CSW-IMG1-SCI0-0001")


def test_6():
    """
    should throw exception if invalid exposure ID: typLevel is missing | CSW-121
    """
    with pytest.raises(ValueError, match="requirement failed: An ExposureId must be a - separated string of the form " +
                                         "SemesterId-ProgramNumber-ObservationNumber-Subsystem-DET-TYPLevel-ExposureNumber"):
        ExposureId.make("2020A-001-123-CSW-IMG1-0001")
    with pytest.raises(KeyError,
                       match="000 is not a member of Enum \\(SCI, CAL, ARC, IDP, DRK, MDK, FFD, NFF, BIA, TEL, FLX, SKY\\)"):
        ExposureId.make("2020A-001-123-CSW-IMG1-0001-01")


def test_7():
    """
    should create ExposureId with exposure number with helper | CSW-121
    """
    exposureId = ExposureId.make("2020A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.exposureNumber == ExposureNumber(1))
    exposureId2 = ExposureId.withExposureNumber(exposureId, 5)
    assert (exposureId2.exposureNumber == ExposureNumber(5))
    assert (exposureId2 == ExposureIdWithObsId(ObsId.make("2020A-001-123"), Subsystem.CSW, "IMG1",
                                               TYPLevel.make("SCI0"), ExposureNumber.make("0005")))


def test_8():
    """
    should increment ExposureId exposure number with helper | CSW-121
    """
    exposureId = ExposureId.make("2020A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.exposureNumber == ExposureNumber(1))
    exposureId2 = ExposureId.nextExposureNumber(exposureId)
    assert (exposureId2.exposureNumber == ExposureNumber(2))
    assert (exposureId2 == ExposureIdWithObsId(ObsId.make("2020A-001-123"), Subsystem.CSW, "IMG1",
                                               TYPLevel.make("SCI0"), ExposureNumber.make("0002")))


def test_9():
    """
    should add subarray or increment subarray in ExposureId with helper | CSW-121
    """
    exposureId = ExposureId.make("2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (str(exposureId) == "2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.exposureNumber == ExposureNumber(1))
    assert (exposureId.exposureNumber.subArray is None)
    # Should add it at 00
    exposureId2 = ExposureId.nextSubArrayNumber(exposureId)
    assert (str(exposureId2) == "2031A-001-123-CSW-IMG1-SCI0-0001-00")
    assert (exposureId2.exposureNumber == ExposureNumber(1, 0))
    assert (exposureId2.exposureNumber.subArray == 0)
    # Should now increment
    exposureId3 = ExposureId.nextSubArrayNumber(exposureId2)
    assert (str(exposureId3) == "2031A-001-123-CSW-IMG1-SCI0-0001-01")
    assert (exposureId3.exposureNumber == ExposureNumber(1, 1))
    assert (exposureId3.exposureNumber.subArray == 1)


def test_10():
    """
    should set subarray to ExposureId with helper | CSW-121
    """
    exposureId = ExposureId.make("2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.exposureNumber == ExposureNumber(1))
    assert (exposureId.exposureNumber.subArray is None)
    # Should set it at 02
    exposureId2 = ExposureId.withSubArrayNumber(exposureId, 2)
    assert (str(exposureId2) == "2031A-001-123-CSW-IMG1-SCI0-0001-02")
    assert (exposureId2.exposureNumber == ExposureNumber(1, 2))
    assert (exposureId2.exposureNumber.exposureNumber == 1)
    assert (exposureId2.exposureNumber.subArray == 2)


def test_11():
    """
    should convert with ObsId to standalone ExposureId | CSW-121
    """
    exposureId = ExposureId.make("2031A-001-123-CSW-IMG1-SCI0-0001")
    assert (exposureId.obsId == ObsId.make("2031A-001-123"))
    utcTime = UTCTime.now()
    exposureId2 = ExposureId.withUTC(exposureId, utcTime)
    assert (exposureId2.obsId is None)


def test_12():
    """
    should convert without ObsId to ExposureId with ObsId | CSW-121
    """
    exposureId = ExposureId.make("CSW-IMG1-SCI0-0001")
    assert (exposureId.obsId is None)
    exposureId2 = ExposureId.withObsId(exposureId, ObsId.make("2031A-001-123"))
    assert (exposureId2.obsId == ObsId.make("2031A-001-123"))


def test_13():
    """
    should verify String format for standalone ExposureId | CSW-121
    """
    # Make up a date time for creating standalone
    utcTime       = UTCTime.from_str("1980-04-09T15:30:45.123Z")
    utcTimeString = ExposureId.utcAsStandaloneString(utcTime)
    assert(len(utcTimeString) == 15)
    assert(utcTimeString == "19800409-153045")
