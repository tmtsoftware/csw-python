from csw_protobuf.parameter_types_pb2 import IntItems, LongItems, ShortItems, FloatItems, DoubleItems, CharItems, \
    ByteItems


# --- Wrappers for protobuf array items ---

class IntArray:
    def __init__(self, values):
        """
        Wrapper for IntArrayItems: values should be an array of array of ints
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = IntItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class LongArray:
    def __init__(self, values):
        """
        Wrapper for LongArrayItems: values should be an array of array of longs
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = LongItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class ShortArray:
    def __init__(self, values):
        """
        Wrapper for ShortArrayItems: values should be an array of array of shorts
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = ShortItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class FloatArray:
    def __init__(self, values):
        """
        Wrapper for FloatArrayItems: values should be an array of array of floats
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = FloatItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class DoubleArray:
    def __init__(self, values):
        """
        Wrapper for DoubleArrayItems: values should be an array of array of doubles
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = DoubleItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class CharArray:
    def __init__(self, values):
        """
        Wrapper for CharArrayItems: values should be an array of array of chars
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = CharItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar

class ByteArray:
    def __init__(self, values):
        """
        Wrapper for ByteArrayItems: values should be an array of array of bytes
        :param list values: list of parameter values
        """
        ar = []
        for i in values:
            item = ByteItems()
            item.values.extend(i)
            ar.append(item)
        self.items = ar
