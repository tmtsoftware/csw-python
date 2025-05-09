import pytest

from csw.SemesterId import SemesterId, Semester


# Create SemesterId
def test_1():
    """
    "should create semesterId with valid year and semester | CSW-121"
    """
    semesterId = SemesterId.make("2010B")
    assert(str(semesterId) == "2010B")
    assert(semesterId.year == 2010)
    assert(semesterId.semester == Semester.B)

def test_2():
    "should throw exception if semester is invalid | CSW-121"
    with pytest.raises(ValueError):
        SemesterId.make("2010C")

# def test_3():
#     "should throw exception if year is invalid | CSW-121"
#     with pytest.raises(ValueError):
#         SemesterId.make("1000000000A")
