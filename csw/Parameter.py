from dataclasses import dataclass

from typing import List

from csw.Coords import Coord

coordTypes = {"CoordKey", "EqCoordKey", "SolarSystemCoordKey", "MinorPlanetCoordKey", "CometCoordKey"}

@dataclass
class Parameter:
    """
    Creates a Parameter (keys with values, units).
    See https://tmtsoftware.github.io/csw/0.7.0-RC1/messages/keys-parameters.html for key type names.
    See https://tmtsoftware.github.io/csw/0.7.0-RC1/messages/units.html for list of unit names.
    'items' is an array of values, or a nested array for array and matrix types. (TODO: changes are planned)
    """
    keyName: str
    keyType: str
    items: object
    units: str = "NoUnits"

    def asDict(self):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array
        if (self.keyType == "ByteKey"):
            items = self.items
        else:
            items = list(map(lambda p: Parameter.paramValueOrDict(self.keyType, p), self.items))
        return {
            'keyName': self.keyName,
            'keyType': self.keyType,
            'items': items,
            'units': self.units
        }

    @staticmethod
    def paramValueOrDict(keyType: str, param):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param param: parameter value, which might be a primitive type or another param for Struct types
        :return: simple param value, or a dictionary if keytype is StructKey
        """
        if keyType in coordTypes.union({"StructKey"}):
            return param.asDict()
        else:
            return param

    @staticmethod
    def paramValueFromDict(keyType, obj):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param obj: parameter value, which might be a primitive type or another param for Struct types
        :return: simple param value, or a Struct object if keytype is StructKey
        """
        if keyType == "StructKey":
            return Struct.fromDict(obj)
        elif keyType in coordTypes:
            return Coord.fromDict(obj)
        else:
            return obj

    @staticmethod
    def fromDict(obj: dict):
        """
        Returns a Parameter for the given CBOR object.
        """
        keyType = obj['keyType']
        if (keyType == "ByteKey"):
            items = obj['items']
        else:
            items = list(map(lambda p: Parameter.paramValueFromDict(keyType, p), obj['items']))
        return Parameter(obj['keyName'], keyType, items, obj['units'])


# -----------------
# Struct parameter
# -----------------
@dataclass
class Struct:
    """
    Creates a Struct (value when key is "StructKey").
    'paramSet' is a list of Parameters that make up the Struct
    """
    paramSet: List[Parameter]

    def asDict(self):
        return {"paramSet" : list(map(lambda p: p.asDict(), self.paramSet))}

    @staticmethod
    def fromDict(obj: dict):
        return Struct(list(map(lambda p: Parameter.fromDict(p), obj['paramSet'])))
