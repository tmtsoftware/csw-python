import asyncio

from aiohttp import ClientSession

from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import DoubleKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

# Test publishing events

async def main():
    clientSession = ClientSession()
    source = Prefix(Subsystem.CSW, "testassembly")
    eventName = EventName("myAssemblyEvent")
    param = DoubleKey.make("assemblyEventValue").set(42.0)
    paramSet = [param]

    event = SystemEvent(source, eventName, paramSet)
    pub = await EventPublisher.make(clientSession)
    pub.publish(event)

asyncio.run(main())
