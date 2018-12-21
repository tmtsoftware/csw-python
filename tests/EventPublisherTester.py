import unittest

from csw_event.EventSubscriber import EventSubscriber
from csw_event.EventPublisher import EventPublisher
from csw_protobuf.events_pb2 import PbEvent


class EventPublisherTester(unittest.TestCase):

    def test(self):
        pub = EventPublisher()
        sub = EventSubscriber()

        event = PbEvent()

        pub.publish(event)