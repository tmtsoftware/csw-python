import unittest

from csw_event.EventSubscriber import EventSubscriber
from csw_event.EventPublisher import EventPublisher
from csw_event.Parameter import Parameter
from csw_event.Event import Event


class EventPublisherTester(unittest.TestCase):

    def test(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        source = "test.assembly"
        eventName = "myAssemblyEvent"
        eventKey = source + "." + eventName

        keyName = "assemblyEventValue"
        keyType = 'IntKey'
        items = [42]
        param = Parameter(keyName, keyType, items)
        paramSet = [param]

        event = Event(source, eventName, paramSet)

        thread = sub.subscribe([eventKey], self.callback)
        pub.publish(event)
        e = sub.get(eventKey)
        assert (e == event)
        thread.stop()

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.items}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
