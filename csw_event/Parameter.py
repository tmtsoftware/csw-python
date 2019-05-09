from dataclasses import dataclass


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
    items: list
    units: str = "NoUnits"

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return {
            'keyName': self.keyName,
            'keyType': self.keyType,
            'items': self.items,
            'units': self.units
        }

    @staticmethod
    def deserialize(obj):
        """
        Returns a Parameter for the given CBOR object.
        """
        return Parameter(obj['keyName'], obj['keyType'], obj['items'], obj['units'])
