import unittest

from csw_event.EventSubscriber import EventSubscriber
from csw_event.EventPublisher import EventPublisher
from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent


class EventPublisherTester(unittest.TestCase):

    def test(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        source = "test.assembly"
        eventName = "myAssemblyEvent"

        keyName = "assemblyEventValue"
        keyType = 'IntKey'
        items = [42]
        param = Parameter(keyName, keyType, items)
        paramSet = [param]

        event = SystemEvent(source, eventName, paramSet)

        pub.publish(event)