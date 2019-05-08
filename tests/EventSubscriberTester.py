import unittest

from csw_event.EventSubscriber import EventSubscriber
from csw_protobuf.events_pb2 import PbEvent


class EventSubscriberTester(unittest.TestCase):

    def setUp(self):
        self.sub = EventSubscriber()

    def test(self):
        self.sub.subscribe(['a.b.c', 'a.b.myevent'], self.callbackEvent)

    @staticmethod
    def callback(message):
        print("Callback:", message)
        event = PbEvent()
        event.ParseFromString(message['data'])
        print(event.eventName)

    @staticmethod
    def callbackEvent(event):
        print(event.eventName)

    def testGet(self):
        ev = self.sub.get('a.b.c')
        event = PbEvent()
        event.ParseFromString(ev)
        print(event.eventName)

