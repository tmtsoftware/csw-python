from csw_protobuf.keytype_pb2 import IntKey, StringKey, ChoiceKey, RaDecKey, StructKey, BooleanKey, ByteKey, CharKey, \
    ShortKey, LongKey, FloatKey, DoubleKey, TimestampKey, ByteArrayKey, ShortArrayKey, LongArrayKey, IntArrayKey, \
    FloatArrayKey, DoubleArrayKey, ByteMatrixKey, ShortMatrixKey, LongMatrixKey, IntMatrixKey, FloatMatrixKey, \
    DoubleMatrixKey
from csw_protobuf.parameter_pb2 import PbParameter
from csw_protobuf.units_pb2 import NoUnits

class Parameter:

    # Depending on the key type, set a different field in the parameter p to the list of items i.
    __itemSetters__ = {
        ChoiceKey: lambda p, i: p.choiceItems.values.extend(i),
        RaDecKey: lambda p, i: p.raDecItems.values.extend(i),
        StringKey: lambda p, i: p.stringItems.values.extend(i),
        StructKey: lambda p, i: p.structItems.values.extend(i),
        BooleanKey: lambda p, i: p.booleanItems.values.extend(i),
        ByteKey: lambda p, i: p.byteItems.values.extend(i),
        CharKey: lambda p, i: p.charItems.values.extend(i),
        ShortKey: lambda p, i: p.shortItems.values.extend(i),
        LongKey: lambda p, i: p.longItems.values.extend(i),
        IntKey: lambda p, i: p.intItems.values.extend(i),
        FloatKey: lambda p, i: p.floatItems.values.extend(i),
        DoubleKey: lambda p, i: p.doubleItems.values.extend(i),
        TimestampKey: lambda p, i: p.instantItems.values.extend(i),
        ByteArrayKey: lambda p, i: p.byteArrayItems.values.extend(i),
        ShortArrayKey: lambda p, i: p.shortArrayItems.values.extend(i),
        LongArrayKey: lambda p, i: p.longArrayItems.values.extend(i),
        IntArrayKey: lambda p, i: p.intArrayItems.values.extend(i),
        FloatArrayKey: lambda p, i: p.floatArrayItems.values.extend(i),
        DoubleArrayKey: lambda p, i: p.doubleArrayItems.values.extend(i),
        ByteMatrixKey: lambda p, i: p.byteMatrixItems.values.extend(i),
        ShortMatrixKey: lambda p, i: p.shortMatrixItems.values.extend(i),
        LongMatrixKey: lambda p, i: p.longMatrixItems.values.extend(i),
        IntMatrixKey: lambda p, i: p.intMatrixItems.values.extend(i),
        FloatMatrixKey: lambda p, i: p.floatMatrixItems.values.extend(i),
        DoubleMatrixKey: lambda p, i: p.doubleMatrixItems.values.extend(i),
    }

    # Depending on the key type, get a different field in the parameter p as a list of items.
    __itemGetters__ = {
        ChoiceKey: lambda p: p.choiceItems.values,
        RaDecKey: lambda p: p.raDecItems.values,
        StringKey: lambda p: p.stringItems.values,
        StructKey: lambda p: p.structItems.values,
        BooleanKey: lambda p: p.booleanItems.values,
        ByteKey: lambda p: p.byteItems.values,
        CharKey: lambda p: p.charItems.values,
        ShortKey: lambda p: p.shortItems.values,
        LongKey: lambda p: p.longItems.values,
        IntKey: lambda p: p.intItems.values,
        FloatKey: lambda p: p.floatItems.values,
        DoubleKey: lambda p: p.doubleItems.values,
        TimestampKey: lambda p: p.instantItems.values,
        ByteArrayKey: lambda p: p.byteArrayItems.values,
        ShortArrayKey: lambda p: p.shortArrayItems.values,
        LongArrayKey: lambda p: p.longArrayItems.values,
        IntArrayKey: lambda p: p.intArrayItems.values,
        FloatArrayKey: lambda p: p.floatArrayItems.values,
        DoubleArrayKey: lambda p: p.doubleArrayItems.values,
        ByteMatrixKey: lambda p: p.byteMatrixItems.values,
        ShortMatrixKey: lambda p: p.shortMatrixItems.values,
        LongMatrixKey: lambda p: p.longMatrixItems.values,
        IntMatrixKey: lambda p: p.intMatrixItems.values,
        FloatMatrixKey: lambda p: p.floatMatrixItems.values,
        DoubleMatrixKey: lambda p: p.doubleMatrixItems.values,
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
