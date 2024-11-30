from typing import Self

import cbor2
from aiohttp import ClientSession

from csw.Event import Event
from csw.RedisConnector import RedisConnector

# XXX TODO FIXME: Use async redis

class EventPublisher:

    def __init__(self, redis: RedisConnector):
        self._redis = redis

    @classmethod
    async def make(cls, clientSession: ClientSession) -> Self:
        return cls(await RedisConnector.make(clientSession))

    def publish(self, event: Event):
        """
        Publish an event to the Event Service

        Args:
            event (Event): Event to be published
        """
        event_key = str(event.source) + "." + event.eventName.name
        obj = cbor2.dumps(event._asDict())
        self._redis.publish(event_key, obj)
