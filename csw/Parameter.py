from dataclasses import dataclass
from typing import TypeVar, Generic, List

from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.KeyType import KeyType
from csw.Coords import *

coordTypes = {KeyType.CoordKey, KeyType.EqCoordKey, KeyType.SolarSystemCoordKey, KeyType.MinorPlanetCoordKey,
              KeyType.CometCoordKey}
timeKeyTypes = {KeyType.TAITimeKey, KeyType.UTCTimeKey}

T = TypeVar('T')


# noinspection PyProtectedMember
@dataclass
class Parameter(Generic[T]):
    # noinspection PyUnresolvedReferences
    """
        Creates a Parameter (keys with values, units).

        Args:

            keyName (str): name of the key
            keyType (KeyType): type of the key
            values (List[T]): an array of values, or a nested array for array and matrix types.
            units (Units): units of the values.
        """
    keyName: str
    keyType: KeyType
    values: List[T]
    units: Units = Units.NoUnits

    @staticmethod
    def _paramValueOrDict(keyType: KeyType, param: T, forEvent: bool):
        """
        Internal method that also handles coord and time types

        Args:
            keyType (KeyType): parameter's key type
            param (T): parameter value
            forEvent (bool): needed since time values are encoded differently in CBOR and JSON

        Returns:
            param value
        """
        # keyTypes = coordTypes.union(timeKeyTypes) if forEvent else coordTypes
        if keyType in coordTypes:
            return param._asDict()
        if keyType in timeKeyTypes:
            if forEvent:
                return param._asDict()
            return str(param)
        return param

    @staticmethod
    def _paramValueFromDict(keyType: KeyType, obj: T, forEvent: bool) -> T:
        """
        Internal recursive method that also handles Coord types

        Args:

            keyType (KeyType): parameter's key type
            obj: T
            forEvent (bool): needed since time values are encoded differently in CBOR and JSON

        Returns: object
            param value
        """
        if keyType in coordTypes:
            return Coord._fromDict(obj)
        elif not forEvent and keyType in timeKeyTypes:
            if keyType == KeyType.UTCTimeKey:
                return UTCTime.from_str(obj)
            else:
                return TAITime.from_str(obj)
        else:
            return obj

    # noinspection PyTypeChecker
    # forEvent flag is needed since time and byte values are encoded differently in CBOR and JSON
    def _asDict(self, forEvent: bool = False):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array.
        if forEvent and self.keyType == KeyType.ByteKey:
            values = bytes(self.values)
        else:
            values = list(map(lambda p: Parameter._paramValueOrDict(self.keyType, p, forEvent), self.values))

        return {
            self.keyType.name: {
                'keyName': self.keyName,
                'values': values,
                'units': self.units.name
            }
        }

    @staticmethod
    # forEvent flag is needed since time values are encoded differently in CBOR and JSON
    def _fromDict(obj: dict, forEvent: bool = False):
        """
        Returns a Parameter for the given dict.
        """
        k = next(iter(obj))
        keyType = KeyType[k]
        obj = obj[k]

        if forEvent and keyType == KeyType.ByteKey:
            values = list(obj['values'])
        else:
            values = list(map(lambda p: Parameter._paramValueFromDict(keyType, p, forEvent), obj['values']))
        return Parameter(obj['keyName'], keyType, values, Units[obj['units']])


@dataclass
class Key(Generic[T]):
    keyName: str
    keyType: KeyType
    units: Units

    def set(self, *values: T) -> Parameter[T]:
        return Parameter(self.keyName, self.keyType, [*values], self.units)

    def setAll(self, values: List[T]) -> Parameter[T]:
        return Parameter(self.keyName, self.keyType, values, self.units)


# noinspection DuplicatedCode
class ChoiceKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[str]:
        return Key(name, KeyType.ChoiceKey, units)


class StringKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[str]:
        return Key(name, KeyType.StringKey, units)


class UTCTimeKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[UTCTime]:
        return Key(name, KeyType.UTCTimeKey, units)


class TAITimeKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[TAITime]:
        return Key(name, KeyType.TAITimeKey, units)


class EqCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[EqCoord]:
        return Key(name, KeyType.EqCoordKey, units)


class CometCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[CometCoord]:
        return Key(name, KeyType.CometCoordKey, units)


class SolarSystemCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[SolarSystemCoord]:
        return Key(name, KeyType.SolarSystemCoordKey, units)


class MinorPlanetCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[MinorPlanetCoord]:
        return Key(name, KeyType.MinorPlanetCoordKey, units)


class AltAzCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[AltAzCoord]:
        return Key(name, KeyType.AltAzCoordKey, units)


class CoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[Coord]:
        return Key(name, KeyType.CoordKey, units)


# noinspection DuplicatedCode
class BooleanKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[bool]:
        return Key(name, KeyType.BooleanKey, units)


class CharKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[str]:
        return Key(name, KeyType.CharKey, units)


class ByteKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.ByteKey, units)


class ShortKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.ShortKey, units)


class LongKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.LongKey, units)


class IntKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.IntKey, units)


class FloatKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[float]:
        return Key(name, KeyType.FloatKey, units)


class DoubleKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[float]:
        return Key(name, KeyType.DoubleKey, units)


class ByteArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[bytes]:
        return Key(name, KeyType.ByteArrayKey, units)


class ShortArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.ShortArrayKey, units)


class LongArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyType.LongArrayKey, units)


class IntArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
        return Key(name, KeyType.IntArrayKey, units)


class FloatArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
        return Key(name, KeyType.FloatArrayKey, units)


class DoubleArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
        return Key(name, KeyType.DoubleArrayKey, units)


# noinspection DuplicatedCode
class ByteMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyType.ByteMatrixKey, units)


class ShortMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyType.ShortMatrixKey, units)


class LongMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyType.LongMatrixKey, units)


class IntMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyType.IntMatrixKey, units)


class FloatMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[float]]]:
        return Key(name, KeyType.FloatMatrixKey, units)


class DoubleMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyType.DoubleMatrixKey, units)
