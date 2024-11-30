import time

import structlog
from aiohttp import ClientSession

from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Parameter import IntKey
from csw.Event import SystemEvent, EventName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from csw.EventKey import EventKey


class TestEventPublisher:
    log = structlog.get_logger()
    count = 0
    clientSession = ClientSession()

    # Simple test that publishes an event and subscribes to it
    # Requires that CSW services are running.
    async def test_pub_sub(self):
        pub = await EventPublisher.make(self.clientSession)
        sub = await EventSubscriber.make(self.clientSession)

        prefix = Prefix(Subsystem.CSW, "assembly")
        eventName = EventName("test_event")
        eventKey = EventKey(prefix, eventName)
        param = IntKey.make("testEventValue").set(42)
        paramSet = [param]
        event = SystemEvent(prefix, eventName, paramSet)

        subscription = await sub.subscribe([eventKey], self.callback)
        await pub.publish(event)
        time.sleep(1)
        e = await sub.get(eventKey)
        assert (e == event)
        assert (self.count == 1)
        await sub.unsubscribe([eventKey])
        await subscription.unsubscribe()

    async def callback(self, systemEvent):
        self.count = self.count + 1
        self.log.debug(f"Received system event '{systemEvent.eventName.name}'")
        for i in systemEvent.paramSet:
            self.log.debug(f"    with values: {i.keyName}: {i.values}")
        if systemEvent.isInvalid():
            self.log.debug("    Invalid")
        if systemEvent.exists("testEventValue"):
            p = systemEvent.get("testEventValue")
            if p is not None:
                self.log.debug(f"Found: {p.keyName}")
