
class Parameter:

    def __init__(self, keyName, keyType, items, units = "NoUnits"):
        """
        Creates a Parameter (keys with values, units).

        :param str keyName: the name of the key
        :param str keyType: the type of the key (One of TODO: document types)
        :param list items: a list of values of the given type (matching the key type)
        :param int units: units of the values (one of the PbUnits enum values, default NoUnits)
        """

        self.keyName = keyName
        self.keyType = keyType
        self.items = items
        self.units = units

    @staticmethod
    def deserialize(obj):
        """
        Returns a Parameter for the given CBOR object.
        """
        return Parameter(obj['keyName'], obj['keyType'], obj['items'], obj['units'])

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

