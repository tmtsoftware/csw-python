import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.Event import SystemEvent


class TestEventPublisher:
    count = 0

    # Simple test that publishes an event and subscribes to it
    # Requires that CSW services are running.
    def test_pub_sub(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        prefix = "CSW.assembly"
        eventName = "test_event"
        eventKey = prefix + "." + eventName
        keyName = "testEventValue"
        keyType = 'IntKey'
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
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("testEventValue"):
            p = systemEvent.get("testEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
