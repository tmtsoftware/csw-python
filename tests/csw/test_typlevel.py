import pytest

from csw.TYPLevel import TYPLevel, TYPs, CalibrationLevel


def test_1():
    """
    should create TYPLevel | CSW-121
    """
    typLevel = TYPLevel.make("SCI0")
    assert (str(typLevel) == "SCI0")
    assert (typLevel == TYPLevel(TYPs.SCI, CalibrationLevel.Raw))
    assert (typLevel.calibrationLevel == CalibrationLevel.Raw)
    assert (typLevel.calibrationLevelNumber() == 0)


def test_2():
    """
    should throw exception if invalid TYP | CSW-121
    """
    with pytest.raises(KeyError):
        TYPLevel.make("XYZ0")


def test_3():
    """
    should throw exception if invalid calibrationLevel | CSW-121
    """
    with pytest.raises(ValueError,
                       match="Failed to parse calibration level 5.*"):
        TYPLevel.make("SCI5")


def test_4():
    """
    should throw exception if no calibrationLevel | CSW-121
    """
    with pytest.raises(ValueError,
                       match="requirement failed: TYPLevel must be a 3 character TYP followed by a calibration level"):
        TYPLevel.make("SCI")


def test_5():
    """
    should throw exception if calibrationLevel is char | CSW-121
    """
    with pytest.raises(ValueError,
                       match="Failed to parse calibration level C.*"):
        TYPLevel.make("SCIC")
