from csw_event.Parameter import Parameter, Struct
from csw_event.Event import Event
from csw_event.EventPublisher import EventPublisher


# Test publishing events
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        floatParam = Parameter("floatValue", "FloatKey", [float(42.1)], "arcsec")
        longParam = Parameter("longValue", "LongKey", [42], "arcsec")
        shortParam = Parameter("shortValue", "ShortKey", [42], "arcsec")
        byteParam = Parameter("byteValue", "ByteKey", b'\xDE\xAD\xBE\xEF')
        booleanParam = Parameter("booleanValue", "BooleanKey", [True, False], "arcsec")

        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")
        doubleArrayParam = Parameter("DoubleArrayValue", "DoubleArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")

        byteArrayParam = Parameter("ByteArrayValue", "ByteArrayKey", [b'\xDE\xAD\xBE\xEF', b'\x01\x02\x03\x04'])

        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")

        structParam = Parameter("MyStruct", "StructKey", [Struct([intParam, floatParam, longParam, shortParam, booleanParam, intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam])])

        paramSet = [byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam, intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam, structParam]
        event = Event("test.assembly", "myAssemblyEvent", paramSet)
        # event = Event("test.assembly", "myAssemblyEvent", [byteParam])
        self.pub.publish(event)


def main():
    TestPublisher3()


if __name__ == "__main__":
    main()
