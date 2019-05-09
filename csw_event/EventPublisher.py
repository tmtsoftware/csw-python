from csw_event.RedisConnector import RedisConnector
from cbor2 import *


class EventPublisher:

    def __init__(self):
        self.__redis = RedisConnector()

    def publish(self, event):
        """
        Publish an event to the Event Service

        :param Event event: Event to be published
        :return: None
        """
        event_key = event.source + "." + event.eventName
        obj = dumps(event.serialize())
        self.__redis.publish(event_key, obj)
