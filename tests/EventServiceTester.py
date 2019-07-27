import unittest

from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.Event import SystemEvent


class EventPublisherTester(unittest.TestCase):

    def test(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        source = "test.assembly"
        eventName = "myAssemblyEvent"
        eventKey = source + "." + eventName

        keyName = "assemblyEventValue"
        keyType = 'IntKey'
        values = [42]
        param = Parameter(keyName, keyType, values)
        paramSet = [param]

        event = SystemEvent(source, eventName, paramSet)

        thread = sub.subscribe([eventKey], self.callback)
        pub.publish(event)
        e = sub.get(eventKey)
        assert (e == event)
        thread.stop()

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
