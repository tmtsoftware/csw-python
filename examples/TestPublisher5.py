import asyncio


from csw.Event import SystemEvent
from csw.EventName import EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import TAITimeKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

# Test publishing events
from csw.TMTTime import TAITime

async def main():
    prefix = Prefix(Subsystem.CSW, "testassembly")
    eventName = EventName("myAssemblyEvent")

    param = TAITimeKey.make("assemblyEventValue").set(TAITime.now())
    paramSet = [param]

    event = SystemEvent(prefix, eventName, paramSet)
    pub = EventPublisher.make()
    await pub.publish(event)

asyncio.run(main())
