import pytest

from csw.ProgramId import ProgramId
from csw.SemesterId import SemesterId


# Create ProgramId
def test_1():
    """
    should create ProgramId | CSW-121
    """
    programId = ProgramId(SemesterId.make("2030A"), 1)
    assert (programId == ProgramId.make("2030A-001"))
    assert (programId.semesterId == SemesterId.make("2030A"))
    assert (programId.programNumber == 1)
    assert (str(programId) == "2030A-001")


def test_2():
    """
    should throw exception if invalid program id | CSW-121
    """
    with pytest.raises(ValueError, match = "requirement failed: Program Number should be integer in the range of 1 to 999"):
        ProgramId.make("2020A-1234")

def test_3():
    """
    should throw exception if invalid semester in SemesterId | CSW-121"
    """
    with pytest.raises(ValueError, match = "Failed to parse semester C: C is not a member of Enum.*"):
        ProgramId.make("202C-123")

def test_4():
    """
    "should throw exception if program id is invalid | CSW-121"
    """
    with pytest.raises(ValueError, match = "A program Id consists of a semester Id and program number separated by '-', ex: 2020A-001"):
        ProgramId.make("2020A-001-123")

