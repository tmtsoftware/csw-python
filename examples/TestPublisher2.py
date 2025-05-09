import asyncio

from csw.Parameter import IntKey, IntArrayKey, FloatArrayKey, IntMatrixKey
from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Units import Units
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


# Test publishing events using the Parameter and Event wrapper classes
class TestPublisher2:

    def __init__(self):
        self.pub = EventPublisher.make()
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue").set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        prefix = Prefix(Subsystem.CSW, "testassembly")
        eventName = EventName("myAssemblyEvent")
        self.event = SystemEvent(prefix, eventName, paramSet)

    async def publish(self):
        await self.pub.publish(self.event)


async def main():
    test = TestPublisher2()

asyncio.run(main())
