import cbor2

from csw.Event import Event
from csw.RedisConnector import RedisConnector


class EventPublisher:

    def __init__(self):
        self.__redis = RedisConnector()

    def publish(self, event: Event):
        """
        Publish an event to the Event Service

        Args:
            event (Event): Event to be published
        """
        event_key = event.source + "." + event.eventName
        obj = cbor2.dumps(event._asDict())
        self.__redis.publish(event_key, obj)
