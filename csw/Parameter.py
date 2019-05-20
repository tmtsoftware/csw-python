from dataclasses import dataclass, asdict

from typing import List


@dataclass(frozen=True)
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

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        # Note that bytes are stored in a byte string (b'...') instead of a list or array
        if (self.keyType == "ByteKey"):
            items = self.items
        else:
            items = list(map(lambda p: Parameter.serializeParamValue(self.keyType, p), self.items))
        return asdict(self)

    @staticmethod
    def serializeParamValue(keyType, param):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param param: parameter value, which might be a primitive type or another param for Struct types
        :return: param value, or a dictionary if keytype is StructKey
        """
        if keyType == "StructKey":
            return param.serialize()
        else:
            return param

    @staticmethod
    def deserializeParamValue(keyType, obj):
        """
        Internal recursive method that handles StructKey types
        :param keyType: parameter's key type
        :param obj: parameter value, which might be a primitive type or another param for Struct types
        :return: param value, or a list of Parameter object if keytype is StructKey
        """
        if keyType == "StructKey":
            return Struct.deserialize(obj)
        else:
            return obj

    @staticmethod
    def deserialize(obj):
        """
        Returns a Parameter for the given CBOR object.
        """
        keyType = obj['keyType']
        if (keyType == "ByteKey"):
            items = obj['items']
        else:
            items = list(map(lambda p: Parameter.deserializeParamValue(keyType, p), obj['items']))
        return Parameter(obj['keyName'], keyType, items, obj['units'])


# -----------------
# Struct parameter
# -----------------
@dataclass(frozen=True)
class Struct:
    """
    Creates a Struct (value when key is "StructKey").
    'paramSet' is a list of Parameters that make up the Struct
    """
    paramSet: List[Parameter]

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return {"paramSet" : list(map(lambda p: p.serialize(), self.paramSet))}

    @staticmethod
    def deserialize(obj):
        """
        Returns a Stuct for the given (decoded) CBOR object.
        """
        return Struct(list(map(lambda p: Parameter.deserialize(p), obj['paramSet'])))
