import pytest

from csw.ExposureNumber import ExposureNumber


def test_1():
    """
    should create valid ExposureNumber | CSW-121
    """
    exposureNumber = ExposureNumber.make("0001")
    assert (exposureNumber == ExposureNumber(1))
    assert (str(exposureNumber) == "0001")


def test_2():
    """
    should create valid ExposureNumber with subArray | CSW-121
    """
    exposureNumber = ExposureNumber.make("0001-01")
    assert (exposureNumber == ExposureNumber(1, 1))
    assert (str(exposureNumber) == "0001-01")


def test_3():
    """
    should throw exception if ExposureNumber is invalid | CSW-121
    """
    with pytest.raises(ValueError,
                       match="requirement failed: Invalid exposure number: 10000. An ExposureNumber must be a 4 digit number and optional 2 digit sub array in format XXXX or XXXX-XX"):
        ExposureNumber.make("10000")

def test_4():
    """
    should throw exception if subarray in exposure number is invalid | CSW-121
    """
    with pytest.raises(ValueError):
        ExposureNumber.make("0002-123")

def test_5():
    """
    should throw exception if exposure number contains more than one '-'  | CSW-121"
    """
    with pytest.raises(ValueError):
        ExposureNumber.make("0001-01-hhhs")
