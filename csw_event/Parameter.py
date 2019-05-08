
class Parameter:

    def __init__(self, keyName, keyType, items, units = "NoUnits"):
        """
        Creates a Parameter (keys with values, units).

        :param str keyName: the name of the key
        :param str keyType: the type of the key (Example: IntKey, StringKey: See https://tmtsoftware.github.io/csw/0.7.0-RC1/messages/keys-parameters.html for key type names)
        :param list items: a list of values of the given type (matching the key type)
        :param str units: units of the values (See https://tmtsoftware.github.io/csw/0.7.0-RC1/messages/units.html for list of unit names)
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

