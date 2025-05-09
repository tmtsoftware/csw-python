import pytest

from csw.ObsId import ObsId
from csw.ProgramId import ProgramId


# Create ObsId
def test_1():
    """
    should create valid obsId | CSW-121
    """
    obsId = ObsId.make("2020A-001-123")
    assert (obsId.programId == ProgramId.make("2020A-001"))
    assert (obsId.observationNumber == 123)
    assert (str(obsId) == "2020A-001-123")


def test_2():
    """
    should throw exception if program Id is invalid | CSW-121
    """
    with pytest.raises(ValueError,
                       match="requirement failed: Program Number should be integer in the range of 1 to 999"):
        ObsId.make("2020A-1234-123")


def test_3():
    """
    should throw exception if observation number is invalid | CSW-121
    """
    with pytest.raises(ValueError,
                       match="requirement failed: Observation Number should be integer in the range of 1 to 999"):
        ObsId.make("2020A-001-2334")


def test_4():
    """
    should throw exception if observation id is invalid | CSW-121
    """
    with pytest.raises(ValueError,
                       match="An ObsId must consist of a semesterId, programNumber, and observationNumber separated by '-', ex: 2020A-001-123"):
        ObsId.make("2020A-001")
