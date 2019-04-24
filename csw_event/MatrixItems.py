# --- Wrappers for protobuf matrix items ---
from csw_event.ArrayItems import IntArray, ByteArray, LongArray, ShortArray, FloatArray, DoubleArray
from csw_protobuf.parameter_pb2 import IntArrayItems, ByteArrayItems, LongArrayItems, ShortArrayItems, \
    FloatArrayItems, DoubleArrayItems


class IntMatrix:
    def __init__(self, values):
        """
        Wrapper for IntMatrixItems: values should be an array of array of array of ints
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = IntArrayItems()
            item.values.extend(IntArray(i).items)
            ar.append(item)
        self.items = ar


class LongMatrix:
    def __init__(self, values):
        """
        Wrapper for LongMatrixItems: values should be an array of array of array of longs
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = LongArrayItems()
            item.values.extend(LongArray(i).items)
            ar.append(item)
        self.items = ar


class ShortMatrix:
    def __init__(self, values):
        """
        Wrapper for ShortMatrixItems: values should be an array of array of array of shorts
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = ShortArrayItems()
            item.values.extend(ShortArray(i).items)
            ar.append(item)
        self.items = ar


class FloatMatrix:
    def __init__(self, values):
        """
        Wrapper for FloatMatrixItems: values should be an array of array of array of floats
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = FloatArrayItems()
            item.values.extend(FloatArray(i).items)
            ar.append(item)
        self.items = ar


class DoubleMatrix:
    def __init__(self, values):
        """
        Wrapper for DoubleMatrixItems: values should be an array of array of array of doubles
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = DoubleArrayItems()
            item.values.extend(DoubleArray(i).items)
            ar.append(item)
        self.items = ar


class ByteMatrix:
    def __init__(self, values):
        """
        Wrapper for ByteMatrixItems: values should be an array of array of array of bytes
        :param list values: list of parameter values (each value is a matrix)
        """
        ar = []
        for i in values:
            item = ByteArrayItems()
            item.values.extend(ByteArray(i).items)
            ar.append(item)
        self.items = ar
