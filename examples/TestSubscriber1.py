import asyncio

from aiohttp import ClientSession

from csw.Event import Event, EventName
from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber1:

    def __init__(self, eventSubscriber: EventSubscriber):
        self.eventSubscriber = eventSubscriber
        self.count = 0
        self.eventKey = EventKey(Prefix(Subsystem.CSW, "testassembly"), EventName("myAssemblyEvent"))
        self.eventSubscription = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, event: Event):
        print(f"Event = {event} (Event Time = {str(event.eventTime)}")
        self.count = self.count + 1
        if (self.count > 4):
            self.eventSubscriber.unsubscribe([self.eventKey])
            self.eventSubscription.unsubscribe()


async def main():
    clientSession = ClientSession()
    eventSubscriber = await EventSubscriber.make(clientSession)
    TestSubscriber1(eventSubscriber)


asyncio.run(main())
