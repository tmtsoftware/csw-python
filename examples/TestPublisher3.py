from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
from csw.Parameter import Parameter
from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.KeyType import KeyType
from csw.Units import Units


# Test publishing events
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
        floatParam = Parameter("floatValue", KeyType.FloatKey, [float(42.1)], Units.arcsec)
        longParam = Parameter("longValue", KeyType.LongKey, [42], Units.arcsec)
        shortParam = Parameter("shortValue", KeyType.ShortKey, [42], Units.arcsec)
        byteParam = Parameter("byteValue", KeyType.ByteKey, b'\xDE\xAD\xBE\xEF')
        booleanParam = Parameter("booleanValue", KeyType.BooleanKey, [True, False], Units.arcsec)

        intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], Units.arcsec)
        doubleArrayParam = Parameter("DoubleArrayValue", KeyType.DoubleArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], Units.arcsec)

        byteArrayParam = Parameter("ByteArrayValue", KeyType.ByteArrayKey, [b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4])])

        intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234,
                                                 "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = Parameter("CoordParam", KeyType.CoordKey,
                                [eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord, altAzCoord])

        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam]
        event = SystemEvent("CSW.testassembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)


def main():
    TestPublisher3()


if __name__ == "__main__":
    main()
