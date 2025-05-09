from typing import List

from csw.Coords import EqCoord, SolarSystemCoord, MinorPlanetCoord, CometCoord, AltAzCoord, Coord
from csw.Parameter import LongKey, Key, ShortKey, ByteKey, CharKey, BooleanKey, IntKey, FloatKey, DoubleKey, ChoiceKey, \
    GChoiceKey, EqCoordKey, SolarSystemCoordKey, MinorPlanetCoordKey, CometCoordKey, AltAzCoordKey, CoordKey, StringKey, \
    UTCTimeKey, TAITimeKey, ByteArrayKey, ShortArrayKey, LongArrayKey, IntArrayKey, FloatArrayKey, DoubleArrayKey, \
    ByteMatrixKey, ShortMatrixKey, LongMatrixKey, IntMatrixKey, FloatMatrixKey, DoubleMatrixKey
from csw.TMTTime import TAITime
from csw.TMTTime import UTCTime
from csw.Units import Units


# ============= Misc Keys ===========

def choiceKey(name: str, choices: List[str]) -> GChoiceKey[str]:
    return ChoiceKey().make(name, choices)

def eqCoordKey(name: str, units: Units = Units.NoUnits) -> Key[EqCoord]:
    return EqCoordKey().make(name, units)

def solarSystemCoordKey(name: str, units: Units = Units.NoUnits) -> Key[SolarSystemCoord]:
    return SolarSystemCoordKey().make(name, units)

def minorPlanetCoordKey(name: str, units: Units = Units.NoUnits) -> Key[MinorPlanetCoord]:
    return MinorPlanetCoordKey().make(name, units)

def cometCoordKey(name: str, units: Units = Units.NoUnits) -> Key[CometCoord]:
    return CometCoordKey().make(name, units)

def altAzCoordKey(name: str, units: Units = Units.NoUnits) -> Key[AltAzCoord]:
    return AltAzCoordKey().make(name, units)

def coordKey(name: str, units: Units = Units.NoUnits) -> Key[Coord]:
    return CoordKey().make(name, units)

def stringKey(name: str, units: Units = Units.NoUnits) -> Key[str]:
    return StringKey().make(name, units)

def utcTimeKey(name: str) -> Key[UTCTime]:
    return UTCTimeKey().make(name)

def taiTimeKey(name: str) -> Key[TAITime]:
    return TAITimeKey().make(name)

# ============= Simple Keys ===========

def booleanKey(name: str) -> Key[bool]:
    return BooleanKey().make(name)

def charKey(name: str, units: Units = Units.NoUnits) -> Key[str]:
    return CharKey().make(name, units)

def byteKey(name: str, units: Units = Units.NoUnits) -> Key[int]:
    return ByteKey().make(name, units)

def shortKey(name: str, units: Units = Units.NoUnits) -> Key[int]:
    return ShortKey().make(name, units)

def longKey(name: str, units: Units = Units.NoUnits) -> Key[int]:
    return LongKey().make(name, units)

def intKey(name: str, units: Units = Units.NoUnits) -> Key[int]:
    return IntKey().make(name, units)

def floatKey(name: str, units: Units = Units.NoUnits) -> Key[float]:
    return FloatKey().make(name, units)

def doubleKey(name: str, units: Units = Units.NoUnits) -> Key[float]:
    return DoubleKey().make(name, units)

# ============= Array Keys ===========
def byteArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[bytes]]:
    return ByteArrayKey().make(name, units)

def shortArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
    return ShortArrayKey().make(name, units)

def longArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
    return LongArrayKey().make(name, units)

def intArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
    return IntArrayKey().make(name, units)

def floatArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
    return FloatArrayKey().make(name, units)

def doubleArrayKey(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
    return DoubleArrayKey().make(name, units)

# ============= Matrix Keys ===========

def byteMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[bytes]]]:
    return ByteMatrixKey().make(name, units)

def shortMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
    return ShortMatrixKey().make(name, units)

def longMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
    return LongMatrixKey().make(name, units)

def intMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
    return IntMatrixKey().make(name, units)

def floatMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[float]]]:
    return FloatMatrixKey().make(name, units)

def doubleMatrixKey(name: str, units: Units = Units.NoUnits) -> Key[List[List[float]]]:
    return DoubleMatrixKey().make(name, units)

# ============= Helpers ===========

# inline fun <reified T> arrayData(elms: Array<T>): ArrayData<T> = ArrayData.fromArray(elms)
#
# inline fun <reified T> arrayData(first: T, vararg rest: T): ArrayData<T> = ArrayData.fromArrays(first, *rest)
#
# inline fun <reified T> matrixData(elms: Array<Array<T>>): MatrixData<T> = MatrixData.fromArrays(elms)
# inline fun <reified T> matrixData(first: Array<T>, vararg rest: Array<T>): MatrixData<T> = MatrixData.fromArrays(first, *rest)
#
# def choicesOf(vararg choices: str): Choices = Choices.from(choices.toSet())


