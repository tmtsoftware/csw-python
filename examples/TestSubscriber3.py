import asyncio

from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from csw.Event import EventName
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        self.eventSubscriber = EventSubscriber.make()
        self.eventKey = EventKey(Prefix(Subsystem.CSW, "testassembly"), EventName("myAssemblyEvent"))

    async def subscribe(self):
        self.subscription = await self.eventSubscriber.subscribe([self.eventKey], self.callback)

    async def callback(self, systemEvent):
        print(f"Received system event '{systemEvent.eventName.name}' with event time: '{systemEvent.eventTime}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}({i.keyType.name}): {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
        await self.subscription.unsubscribe()


async def main():
    test = TestSubscriber3()
    await test.subscribe()


asyncio.run(main())
