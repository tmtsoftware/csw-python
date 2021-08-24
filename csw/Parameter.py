from dataclasses import dataclass

from typing import List

from csw.Coords import Coord

coordTypes = {"CoordKey", "EqCoordKey", "SolarSystemCoordKey", "MinorPlanetCoordKey", "CometCoordKey"}


@dataclass
class Parameter:
    """
    Creates a Parameter (keys with values, units).
    See https://tmtsoftware.github.io/csw/params/keys-parameters.html for key type names.
    See https://tmtsoftware.github.io/csw/params/units.html for list of unit names.

    Args:

        keyName (str): name of the key
        keyType (str): type of the key (see above link)
        values (object): an array of values, or a nested array for array and matrix types.
        units (str): units of the values (see above link).
    """
    keyName: str
    keyType: str
    values: object
    units: str = "NoUnits"

    @staticmethod
    def _paramValueOrDict(keyType: str, param):
        """
        Internal method that also handles coord and time types

        Args:
            keyType (str): parameter's key type
            param: parameter value

        Returns:
            param value
        """
        if keyType in coordTypes.union({"TAITimeKey", "UTCTimeKey"}):
            return param._asDict()
        else:
            return param

    @staticmethod
    def _paramValueFromDict(keyType: str, obj):
        """
        Internal recursive method that also handles Coord types

        Args:

            keyType (str): parameter's key type
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
        if self.keyType == "ByteKey":
            values = self.values
        else:
            values = list(map(lambda p: Parameter._paramValueOrDict(self.keyType, p), self.values))

        return {
            self.keyType: {
                'keyName': self.keyName,
                'values': values,
                'units': self.units
            }
        }

    @staticmethod
    def _fromDict(obj: dict):
        """
        Returns a Parameter for the given dict.
        """
        keyType = next(iter(obj))
        obj = obj[keyType]

        if keyType == "ByteKey":
            values = obj['values']
        else:
            values = list(map(lambda p: Parameter._paramValueFromDict(keyType, p), obj['values']))
        return Parameter(obj['keyName'], keyType, values, obj['units'])


