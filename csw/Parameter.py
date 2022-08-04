# noinspection PyUnresolvedReferences
from dataclasses import dataclass
from typing import TypeVar, Generic, List

from csw.KeyTypes import KeyTypes
from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.Coords import *

coordTypes = {KeyTypes.CoordKey, KeyTypes.EqCoordKey, KeyTypes.SolarSystemCoordKey, KeyTypes.MinorPlanetCoordKey,
              KeyTypes.CometCoordKey}
timeKeyTypes = {KeyTypes.TAITimeKey, KeyTypes.UTCTimeKey}

T = TypeVar('T')


@dataclass
class KeyType(Generic[T]):
    pass


# noinspection PyProtectedMember
@dataclass
class Parameter(Generic[T]):
    # noinspection PyUnresolvedReferences
    """
        Creates a Parameter (keys with values, units).

        Args:

            keyName (str): name of the key
            keyType (KeyTypes): type of the key
            values (List[T]): an array of values, or a nested array for array and matrix types.
            units (Units): units of the values.
        """
    keyName: str
    keyType: KeyTypes
    values: List[T]
    units: Units = Units.NoUnits

    @staticmethod
    def _paramValueOrDict(keyType: KeyTypes, param: T, forEvent: bool):
        """
        Internal method that also handles coord and time types

        Args:
            keyType (KeyTypes): parameter's key type
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
    def _paramValueFromDict(keyType: KeyTypes, obj: T, forEvent: bool) -> T:
        """
        Internal recursive method that also handles Coord types

        Args:

            keyType (KeyTypes): parameter's key type
            obj: T
            forEvent (bool): needed since time values are encoded differently in CBOR and JSON

        Returns: object
            param value
        """
        if keyType in coordTypes:
            return Coord._fromDict(obj)
        elif not forEvent and keyType in timeKeyTypes:
            if keyType == KeyTypes.UTCTimeKey:
                return UTCTime.from_str(obj)
            else:
                return TAITime.from_str(obj)
        else:
            return obj

    # noinspection PyTypeChecker
    # forEvent flag is needed since time and byte values are encoded differently in CBOR and JSON
    def _asDict(self, forEvent: bool = False):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array.
        if forEvent and self.keyType == KeyTypes.ByteKey:
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
        keyType = KeyTypes[k]
        obj = obj[k]

        if forEvent and keyType == KeyTypes.ByteKey:
            values = list(obj['values'])
        else:
            values = list(map(lambda p: Parameter._paramValueFromDict(keyType, p, forEvent), obj['values']))
        return Parameter(obj['keyName'], keyType, values, Units[obj['units']])


# noinspection PyUnresolvedReferences
@dataclass
class Key(Generic[T]):
    """
    A generic Key class. Never meant to be instantiated directly. [[csw.params.core.generics.KeyType]] exposes
    allowed types of Keys and make method to create instances of Key.

    Args:
        keyName: the name of the key
        keyType: reference to an object of type KeyType[S]
        units: applicable units
    """
    keyName: str
    keyType: KeyTypes
    units: Units

    def set(self, *values: T) -> Parameter[T]:
        """
        Set values for this key using variable number of arguments
        Args:
            *values: an Array of values

        Returns:
            an instance of Parameter[T] containing the key name and values

        """
        return Parameter(self.keyName, self.keyType, [*values], self.units)

    def setAll(self, values: List[T]) -> Parameter[T]:
        """
        Set values for this key using a list
        Args:
            *values: an Array of values

        Returns:
            an instance of Parameter[T] containing the key name and values

        """
        return Parameter(self.keyName, self.keyType, values, self.units)


# noinspection PyUnresolvedReferences
@dataclass
class GChoiceKey(Key[T]):
    """
    A key for a choice item similar to an enumeration

    Args:
        keyName: the name of the key
        keyType: reference to an object of type KeyType[S]
        units: applicable units
        choices: the available choices, the values set must be in the choices
    """
    choices: List[str]

    def validate(self, *values: str):
        """
        validates the input list of choices

        Args:
            *values:  one or more values
        """
        assert all(i in self.choices for i in values), \
            f"Bad choice for key: {self.keyName} which must be one of: {self.choices}"

    def set(self, *values: str) -> Parameter[str]:
        self.validate(*values)
        return Parameter(self.keyName, self.keyType, [*values], self.units)

    def setAll(self, values: List[str]) -> Parameter[str]:
        self.validate(*values)
        return Parameter(self.keyName, self.keyType, values, self.units)


# noinspection DuplicatedCode
@dataclass
class ChoiceKey(KeyType[str]):

    @staticmethod
    def make(name: str, choices: List[str]) -> GChoiceKey[str]:
        return GChoiceKey(name, KeyTypes.ChoiceKey, Units.NoUnits, choices)


# noinspection DuplicatedCode
class StringKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[str]:
        return Key(name, KeyTypes.StringKey, units)


class UTCTimeKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[UTCTime]:
        return Key(name, KeyTypes.UTCTimeKey, units)


class TAITimeKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[TAITime]:
        return Key(name, KeyTypes.TAITimeKey, units)


class EqCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[EqCoord]:
        return Key(name, KeyTypes.EqCoordKey, units)


class CometCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[CometCoord]:
        return Key(name, KeyTypes.CometCoordKey, units)


class SolarSystemCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[SolarSystemCoord]:
        return Key(name, KeyTypes.SolarSystemCoordKey, units)


class MinorPlanetCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[MinorPlanetCoord]:
        return Key(name, KeyTypes.MinorPlanetCoordKey, units)


class AltAzCoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[AltAzCoord]:
        return Key(name, KeyTypes.AltAzCoordKey, units)


class CoordKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[Coord]:
        return Key(name, KeyTypes.CoordKey, units)


# noinspection DuplicatedCode
class BooleanKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[bool]:
        return Key(name, KeyTypes.BooleanKey, units)


# noinspection DuplicatedCode
class CharKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[str]:
        return Key(name, KeyTypes.CharKey, units)


class ByteKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyTypes.ByteKey, units)


class ShortKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyTypes.ShortKey, units)


class LongKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyTypes.LongKey, units)


class IntKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[int]:
        return Key(name, KeyTypes.IntKey, units)


class FloatKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[float]:
        return Key(name, KeyTypes.FloatKey, units)


class DoubleKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[float]:
        return Key(name, KeyTypes.DoubleKey, units)


class ByteArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[bytes]]:
        return Key(name, KeyTypes.ByteArrayKey, units)


class ShortArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
        return Key(name, KeyTypes.ShortArrayKey, units)


class LongArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
        return Key(name, KeyTypes.LongArrayKey, units)


class IntArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[int]]:
        return Key(name, KeyTypes.IntArrayKey, units)


class FloatArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
        return Key(name, KeyTypes.FloatArrayKey, units)


class DoubleArrayKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[float]]:
        return Key(name, KeyTypes.DoubleArrayKey, units)


# noinspection DuplicatedCode
class ByteMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyTypes.ByteMatrixKey, units)


class ShortMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyTypes.ShortMatrixKey, units)


class LongMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyTypes.LongMatrixKey, units)


# noinspection DuplicatedCode
class IntMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[int]]]:
        return Key(name, KeyTypes.IntMatrixKey, units)


class FloatMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[float]]]:
        return Key(name, KeyTypes.FloatMatrixKey, units)


class DoubleMatrixKey:
    @staticmethod
    def make(name: str, units: Units = Units.NoUnits) -> Key[List[List[float]]]:
        return Key(name, KeyTypes.DoubleMatrixKey, units)
