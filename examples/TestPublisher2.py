import asyncio

from aiohttp import ClientSession

from csw.Parameter import IntKey, IntArrayKey, FloatArrayKey, IntMatrixKey
from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Units import Units
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from sequencer.EventServiceDsl import EventServiceDsl


# Test publishing events using the Parameter and Event wrapper classes
class TestPublisher2:

    def __init__(self, pub: EventPublisher):
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue").set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        prefix = Prefix(Subsystem.CSW, "testassembly")
        eventName = EventName("myAssemblyEvent")
        event = SystemEvent(prefix, eventName, paramSet)
        pub.publish(event)


async def main():
    clientSession = ClientSession()
    pub = await EventPublisher.make(clientSession)
    TestPublisher2(pub)

asyncio.run(main())
