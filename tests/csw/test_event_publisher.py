import time

import structlog

from csw.KeyType import KeyType
from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.Event import SystemEvent, EventName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from csw.EventKey import EventKey


class TestEventPublisher:
    log = structlog.get_logger()
    count = 0

    # Simple test that publishes an event and subscribes to it
    # Requires that CSW services are running.
    def test_pub_sub(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        prefix = Prefix(Subsystems.CSW, "assembly")
        eventName = EventName("test_event")
        eventKey = EventKey(prefix, eventName)
        keyName = "testEventValue"
        keyType = KeyType.IntKey
        values = [42]
        param = Parameter(keyName, keyType, values)
        paramSet = [param]
        event = SystemEvent(prefix, eventName, paramSet)

        thread = sub.subscribe([eventKey], self.callback)
        pub.publish(event)
        time.sleep(1)
        e = sub.get(eventKey)
        assert (e == event)
        assert (self.count == 1)
        sub.unsubscribe([eventKey])
        thread.stop()

    def callback(self, systemEvent):
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
