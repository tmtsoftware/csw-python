from dataclasses import dataclass

from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.KeyType import KeyType
from csw.Coords import Coord

coordTypes = {KeyType.CoordKey, KeyType.EqCoordKey, KeyType.SolarSystemCoordKey, KeyType.MinorPlanetCoordKey,
              KeyType.CometCoordKey}
timeKeyTypes = {KeyType.TAITimeKey, KeyType.UTCTimeKey}


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
    def _paramValueOrDict(keyType: KeyType, param, forEvent: bool):
        """
        Internal method that also handles coord and time types

        Args:
            keyType (KeyType): parameter's key type
            param: parameter value
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
    def _paramValueFromDict(keyType: KeyType, obj, forEvent: bool):
        """
        Internal recursive method that also handles Coord types

        Args:

            keyType (KeyType): parameter's key type
            obj: parameter value
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
    # forEvent flag is needed since time values are encoded differently in CBOR and JSON
    def _asDict(self, forEvent: bool = False):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array.
        if self.keyType == KeyType.ByteKey:
            values = self.values
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

        if keyType == KeyType.ByteKey:
            values = obj['values']
        else:
            values = list(map(lambda p: Parameter._paramValueFromDict(keyType, p, forEvent), obj['values']))
        return Parameter(obj['keyName'], keyType, values, Units[obj['units']])
