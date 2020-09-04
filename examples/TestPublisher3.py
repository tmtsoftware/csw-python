from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
from csw.Parameter import Parameter, Struct
from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher


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

        byteArrayParam = Parameter("ByteArrayValue", "ByteArrayKey", [b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4])])

        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234,
                                                 "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = Parameter("CoordParam", "CoordKey",
                                [eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord, altAzCoord])

        structParam = Parameter("MyStruct", "StructKey", [Struct(
            [coordsParam, intParam, floatParam, longParam, shortParam, booleanParam, intArrayParam, floatArrayParam,
             doubleArrayParam, intMatrixParam])])

        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam, structParam]
        event = SystemEvent("CSW.testassembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)


def main():
    TestPublisher3()


if __name__ == "__main__":
    main()
