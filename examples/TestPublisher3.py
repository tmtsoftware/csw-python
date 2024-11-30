import asyncio

from aiohttp import ClientSession

from csw.Parameter import *
from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from csw.Units import Units


# Test publishing events
class TestPublisher3:

    def __init__(self, pub: EventPublisher):
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        floatParam = FloatKey.make("floatValue", Units.arcsec).set(42.1)
        longParam = LongKey.make("longValue", Units.arcsec).set(42)
        shortParam = ShortKey.make("shortValue", Units.arcsec).set(42)
        byteParam = ByteKey.make("byteValue").set(0xDE, 0xAD, 0xBE, 0xEF)
        booleanParam = BooleanKey.make("booleanValue").set(True, False)

        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue", Units.arcsec).set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        doubleArrayParam = DoubleArrayKey.make("DoubleArrayValue", Units.arcsec).setAll(
            [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]])
        byteArrayParam = ByteArrayKey.make("ByteArrayValue").set(b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4]))
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234, "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = CoordKey.make("CoordParam").set(eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord,
                                                      altAzCoord)
        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam]

        prefix = Prefix(Subsystem.CSW, "testassembly")
        eventName = EventName("myAssemblyEvent")
        event = SystemEvent(prefix, eventName, paramSet)
        pub.publish(event)


async def main():
    clientSession = ClientSession()
    pub = await EventPublisher.make(clientSession)
    TestPublisher3(pub)


asyncio.run(main())
