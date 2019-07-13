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
    'items' is an array of values, or a nested array for array and matrix types.
    """
    keyName: str
    keyType: str
    items: object
    units: str = "NoUnits"

    # noinspection PyTypeChecker
    def asDict(self, flat: bool):
        # Note that bytes are stored in a byte string (b'...') instead of a list or array
        if self.keyType == "ByteKey":
            items = self.items
        else:
            items = list(map(lambda p: Parameter.paramValueOrDict(self.keyType, p, flat), self.items))

        # FIXME: Hack until CSW JSON and CBOR formats are consistent in using 'items'
        itemsKey = 'values' if flat else 'items'

        return {
            'keyName': self.keyName,
            'keyType': self.keyType,
            itemsKey: items,
            'units': self.units
        }

    @staticmethod
    def paramValueOrDict(keyType: str, param, flat: bool):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param param: parameter value, which might be a primitive type or another param for Struct types
        :param flat: if true, use flat layout with 'type': ...
        :return: simple param value, or a dictionary if keytype is StructKey
        """
        if keyType in coordTypes.union({"StructKey"}):
            return param.asDict(flat)
        else:
            return param

    @staticmethod
    def paramValueFromDict(keyType, obj, flat: bool):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param obj: parameter value, which might be a primitive type or another param for Struct types
        :param flat: if true, use flat layout with 'type': ...
        :return: simple param value, or a Struct object if keytype is StructKey
        """
        if keyType == "StructKey":
            return Struct.fromDict(obj, flat)
        elif keyType in coordTypes:
            return Coord.fromDict(obj, flat=False)
        else:
            return obj

    @staticmethod
    def fromDict(obj: dict, flat: bool):
        """
        Returns a Parameter for the given dict.
        """
        keyType = obj['keyType']

        # FIXME: Hack until CSW JSON and CBOR formats are consistent in using 'items'
        itemsKey = 'values' if flat else 'items'

        if keyType == "ByteKey":
            items = obj[itemsKey]
        else:
            items = list(map(lambda p: Parameter.paramValueFromDict(keyType, p, flat), obj[itemsKey]))
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

    def asDict(self, flat: bool):
        return {"paramSet": list(map(lambda p: p.asDict(flat), self.paramSet))}

    @staticmethod
    def fromDict(obj: dict, flat: bool):
        return Struct(list(map(lambda p: Parameter.fromDict(p, flat), obj['paramSet'])))
