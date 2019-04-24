from csw_protobuf.keytype_pb2 import IntKey, StringKey, ChoiceKey, RaDecKey, StructKey, BooleanKey, ByteKey, CharKey, \
    ShortKey, LongKey, FloatKey, DoubleKey, UTCTimeKey, TAITimeKey, ByteArrayKey, ShortArrayKey, LongArrayKey, IntArrayKey, \
    FloatArrayKey, DoubleArrayKey, ByteMatrixKey, ShortMatrixKey, LongMatrixKey, IntMatrixKey, FloatMatrixKey, \
    DoubleMatrixKey
from csw_protobuf.parameter_pb2 import PbParameter
from csw_protobuf.units_pb2 import NoUnits

class Parameter:

    # Depending on the key type, set a different field in the parameter p to the list of items i.
    __itemSetters__ = {
        ChoiceKey: lambda p, i: p.items.choiceItems.values.extend(i),
        RaDecKey: lambda p, i: p.items.raDecItems.values.extend(i),
        StringKey: lambda p, i: p.items.stringItems.values.extend(i),
        StructKey: lambda p, i: p.items.structItems.values.extend(i),
        BooleanKey: lambda p, i: p.items.booleanItems.values.extend(i),
        ByteKey: lambda p, i: p.items.byteItems.values.extend(i),
        CharKey: lambda p, i: p.items.charItems.values.extend(i),
        ShortKey: lambda p, i: p.items.shortItems.values.extend(i),
        LongKey: lambda p, i: p.items.longItems.values.extend(i),
        IntKey: lambda p, i: p.items.intItems.values.extend(i),
        FloatKey: lambda p, i: p.items.floatItems.values.extend(i),
        DoubleKey: lambda p, i: p.items.doubleItems.values.extend(i),
        UTCTimeKey: lambda p, i: p.items.utcTimeItems.values.extend(i),
        TAITimeKey: lambda p, i: p.items.taiTimeItems.values.extend(i),
        ByteArrayKey: lambda p, i: p.items.byteArrayItems.values.extend(i),
        ShortArrayKey: lambda p, i: p.items.shortArrayItems.values.extend(i),
        LongArrayKey: lambda p, i: p.items.longArrayItems.values.extend(i),
        IntArrayKey: lambda p, i: p.items.intArrayItems.values.extend(i),
        FloatArrayKey: lambda p, i: p.items.floatArrayItems.values.extend(i),
        DoubleArrayKey: lambda p, i: p.items.doubleArrayItems.values.extend(i),
        ByteMatrixKey: lambda p, i: p.items.byteMatrixItems.values.extend(i),
        ShortMatrixKey: lambda p, i: p.items.shortMatrixItems.values.extend(i),
        LongMatrixKey: lambda p, i: p.items.longMatrixItems.values.extend(i),
        IntMatrixKey: lambda p, i: p.items.intMatrixItems.values.extend(i),
        FloatMatrixKey: lambda p, i: p.items.floatMatrixItems.values.extend(i),
        DoubleMatrixKey: lambda p, i: p.items.doubleMatrixItems.values.extend(i),
    }

    # Depending on the key type, get a different field in the parameter p as a list of items.
    __itemGetters__ = {
        ChoiceKey: lambda p: p.items.choiceItems.values,
        RaDecKey: lambda p: p.items.raDecItems.values,
        StringKey: lambda p: p.items.stringItems.values,
        StructKey: lambda p: p.items.structItems.values,
        BooleanKey: lambda p: p.items.booleanItems.values,
        ByteKey: lambda p: p.items.byteItems.values,
        CharKey: lambda p: p.items.charItems.values,
        ShortKey: lambda p: p.items.shortItems.values,
        LongKey: lambda p: p.items.longItems.values,
        IntKey: lambda p: p.items.intItems.values,
        FloatKey: lambda p: p.items.floatItems.values,
        DoubleKey: lambda p: p.items.doubleItems.values,
        UTCTimeKey: lambda p: p.items.utcTimeItems.values,
        TAITimeKey: lambda p: p.items.taiTimeItems.values,
        ByteArrayKey: lambda p: p.items.byteArrayItems.values,
        ShortArrayKey: lambda p: p.items.shortArrayItems.values,
        LongArrayKey: lambda p: p.items.longArrayItems.values,
        IntArrayKey: lambda p: p.items.intArrayItems.values,
        FloatArrayKey: lambda p: p.items.floatArrayItems.values,
        DoubleArrayKey: lambda p: p.items.doubleArrayItems.values,
        ByteMatrixKey: lambda p: p.items.byteMatrixItems.values,
        ShortMatrixKey: lambda p: p.items.shortMatrixItems.values,
        LongMatrixKey: lambda p: p.items.longMatrixItems.values,
        IntMatrixKey: lambda p: p.items.intMatrixItems.values,
        FloatMatrixKey: lambda p: p.items.floatMatrixItems.values,
        DoubleMatrixKey: lambda p: p.items.doubleMatrixItems.values,
    }

    def __init__(self, name, keyType, items, units = NoUnits):
        """
        Creates a Parameter (keys with values, units).

        :param str name: the name of the key
        :param int keyType: the type of the key (one of the PbKeyType enum values)
        :param list items: a list of values of the given type (matching the key type)
        :param int units: units of the values (one of the PbUnits enum values, default NoUnits)
        """

        self.name = name
        self.keyType = keyType
        self.items = items
        self.units = units
        parameter = PbParameter()
        parameter.name = name
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

