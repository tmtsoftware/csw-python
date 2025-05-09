import asyncio

from csw.Event import Event, EventName
from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber1:

    def __init__(self):
        self.eventSubscriber = EventSubscriber.make()
        self.count = 0
        self.eventKey = EventKey(Prefix(Subsystem.CSW, "testassembly"), EventName("myAssemblyEvent"))
        self.eventSubscription = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    async def subscribe(self):
        self.eventSubscription = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    async def callback(self, event: Event):
        print(f"Event = {event} (Event Time = {str(event.eventTime)}")
        self.count = self.count + 1
        if (self.count > 4):
            await self.eventSubscriber.unsubscribe([self.eventKey])


async def main():
    test = TestSubscriber1()
    await test.subscribe()


asyncio.run(main())
