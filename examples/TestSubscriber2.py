import asyncio

from aiohttp import ClientSession

from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from csw.Event import EventName
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber2:

    def __init__(self, eventSubscriber: EventSubscriber):
        self.eventSubscriber = eventSubscriber
        self.eventKey = EventKey(Prefix(Subsystem.CSW, "testassembly"), EventName("myAssemblyEvent"))
        self.count = 0
        self.subscription = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, systemEvent):
        print(f"Received system event '{systemEvent.eventName.name}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
        self.count = self.count + 1
        if (self.count > 4):
            self.subscription.unsubscribe()


async def main():
    clientSession = ClientSession()
    eventSubscriber = await EventSubscriber.make(clientSession)
    TestSubscriber2(eventSubscriber)

asyncio.run(main())
