from dataclasses import dataclass

from typing import List

from csw.Units import Units
from csw.KeyType import KeyType
from csw.Coords import Coord

coordTypes = {KeyType.CoordKey, KeyType.EqCoordKey, KeyType.SolarSystemCoordKey, KeyType.MinorPlanetCoordKey, KeyType.CometCoordKey}


@dataclass
class Parameter:
    """
    Creates a Parameter (keys with values, units).

    Args:

        keyName (str): name of the key
        keyType (KeyType): type of the key
        values (object): an array of values, or a nested array for array and matrix types.
        units (Units): units of the values.
    """
    keyName: str
    keyType: KeyType
    values: object
    units: Units = Units.NoUnits

    @staticmethod
    def _paramValueOrDict(keyType: KeyType, param):
        """
        Internal method that also handles coord and time types

        Args:
            keyType (KeyType): parameter's key type
            param: parameter value

        Returns:
            param value
        """
        if keyType in coordTypes.union({KeyType.TAITimeKey, KeyType.UTCTimeKey}):
            return param._asDict()
        else:
            return param

    @staticmethod
    def _paramValueFromDict(keyType: KeyType, obj):
        """
        Internal recursive method that also handles Coord types

        Args:

            keyType (KeyType): parameter's key type
            obj: parameter value

        Returns: object
            param value
        """
        if keyType in coordTypes:
            return Coord._fromDict(obj)
        else:
            return obj

    # noinspection PyTypeChecker
    def _asDict(self):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array
        if self.keyType == KeyType.ByteKey:
            values = self.values
        else:
            values = list(map(lambda p: Parameter._paramValueOrDict(self.keyType, p), self.values))

        return {
            self.keyType.name: {
                'keyName': self.keyName,
                'values': values,
                'units': self.units.name
            }
        }

    @staticmethod
    def _fromDict(obj: dict):
        """
        Returns a Parameter for the given dict.
        """
        k = next(iter(obj))
        keyType = KeyType[k]
        obj = obj[k]

        if keyType == KeyType.ByteKey:
            values = obj['values']
        else:
            values = list(map(lambda p: Parameter._paramValueFromDict(keyType, p), obj['values']))
        return Parameter(obj['keyName'], keyType, values, Units[obj['units']])


