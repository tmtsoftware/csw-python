from csw_protobuf.keytype_pb2 import IntKey, StringKey
from csw_protobuf.parameter_pb2 import PbParameter
from csw_protobuf.units_pb2 import NoUnits

class Parameter:

# XXX TODO: Add support for all these item types in the two tables below
    # ChoiceKey = 0
    # RaDecKey = 1
    # StringKey = 2
    # StructKey = 3
    # BooleanKey = 4
    # ByteKey = 5
    # CharKey = 6
    # ShortKey = 7
    # LongKey = 8
    # IntKey = 9
    # FloatKey = 10
    # DoubleKey = 11
    # TimestampKey = 12
    # ByteArrayKey = 13
    # ShortArrayKey = 14
    # LongArrayKey = 15
    # IntArrayKey = 16
    # FloatArrayKey = 17
    # DoubleArrayKey = 18
    # ByteMatrixKey = 19
    # ShortMatrixKey = 20
    # LongMatrixKey = 21
    # IntMatrixKey = 22
    # FloatMatrixKey = 23
    # DoubleMatrixKey = 24


    # Depending on the key type, set a different field in the parameter p to the list of items i.
    __itemSetters__ = {
        StringKey: lambda p, i: p.stringItems.values.extend(i),
        IntKey: lambda p, i: p.intItems.values.extend(i),
    }

    # Depending on the key type, get a different field in the parameter p as a list of items.
    __itemGetters__ = {
        StringKey: lambda p: p.stringItems.values,
        IntKey: lambda p: p.intItems.values,
    }

    def __init__(self, keyName, keyType, items, units = NoUnits):
        """
        Creates a Parameter (keys with values, units).

        Parameters
        ----------
        keyName : str
            the name of the key
        keyType : int
            the type of the key (one of the PbKeyType enum values)
        items : list
            a list of values of the given type (matching the key type)
        units : int
           units of the values (one of the PbUnits enum values, default NoUnits)
        """
        self.keyName = keyName
        self.keyType = keyType
        self.items = items
        self.units = units
        parameter = PbParameter()
        parameter.name = keyName
        parameter.units = units
        parameter.keyType = keyType
        self.__itemSetters__.get(keyType)(parameter, items)
        self.pbParameter = parameter

    @staticmethod
    def fromPbParameter(p):
        """
        Returns a Parameter for the given PbParameter.
        """
        items = Parameter.__itemGetters__.get(p.keyType)(p)
        return Parameter(p.name, p.keyType, items, p.units)
