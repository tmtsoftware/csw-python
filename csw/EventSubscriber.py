import asyncio
from typing import Callable, Set, Self, Awaitable, List

import cbor2

from csw.EventSubscription import EventSubscription
from csw.RedisConnector import RedisConnector
from csw.Event import Event, SystemEvent
from csw.EventKey import EventKey


# XXX TODO FIXME: Use async redis

class EventSubscriber:

    def __init__(self, redis: RedisConnector):
        self._redis = redis

    @classmethod
    def make(cls) -> Self:
        return cls(RedisConnector.make())

    async def close(self):
        await self._redis.close()

    @staticmethod
    async def _handleCallback(message: dict, callback: Callable[[Event], Awaitable]):
        data = message['data']
        event = Event._fromDict(cbor2.loads(data))
        await callback(event)

    async def subscribe(self, eventKeyList: list[EventKey],
                        callback: Callable[[Event], Awaitable]) -> EventSubscription:
        """
        Start a subscription to system events in event service, specifying a callback
        to be called when an event in the list has its value updated.

        Args:
            eventKeyList (list[EventKey]): list of event EventKey to subscribe to
            callback (Callable[[Event], None]): function to be called when event updates. Should take Event and return void

        Returns:
            an object that can be used to unsubscribe
        """
        keyList = list(map(lambda k: str(k), eventKeyList))

        async def f(message):
            await self._handleCallback(message, callback)

        t = await self._redis.subscribe(keyList, f)
        async def unsub():
            await self._redis.unsubscribe(keyList)
        return EventSubscription(t, unsub)

    async def unsubscribe(self, eventKeyList: list[EventKey]):
        """
        Unsubscribes to the given list of event keys (or all keys, if eventKeyList is empty)

        Args:
            eventKeyList (list[EventKey]): list of EventKeys to unsubscribe from
        """
        keyList = list(map(lambda k: str(k), eventKeyList))
        return await self._redis.unsubscribe(keyList)

    # XXX Commented out due to Event Service performance concerns when using psubscribe
    # def pSubscribe(self, eventKeyList: list, callback):
    #     """
    #     Start a subscription to system events in event service, specifying a callback
    #     to be called when an event in the list has its value updated.
    #     In this case the keys are treated as glob-style patterns:
    #     h?llo subscribes to hello, hallo and hxllo,
    #     h*llo subscribes to hllo and heeeello,
    #     h[ae]llo subscribes to hello and hallo, but not hillo.
    #
    #     Args:
    #         eventKeyList (list): list of event key (string patterns) to subscribe to
    #         callback (function): function to be called when event updates. Should take Event and return void
    #
    #     Returns: PubSubWorkerThread
    #         subscription thread. Use .stop() method to stop subscription.
    #     """
    #     return self._redis.pSubscribe(eventKeyList, lambda message: self._handleCallback(message, callback))

    # def pUnsubscribe(self, eventKeyList: list):
    #     """
    #     Unsubscribes to the given list of event key patterns (or all keys, if eventKeyList is empty)
    #
    #     Args:
    #         eventKeyList (list): list of event key patterns (Strings) to unsubscribe from
    #     """
    #     return self._redis.pUnsubscribe(eventKeyList)

    async def gets(self, eventKeys: Set[EventKey]) -> Set[Event]:
        """
        Get latest events for multiple Event Keys. The latest events available for the given Event Keys will be received first.
        If event is not published for one or more event keys, `invalid event` will be received for those Event Keys.

        In case the underlying server is not available, the future fails with [[csw.event.api.exceptions.EventServerNotAvailable]] exception.
        In all other cases of exception, the future fails with the respective exception

        Args:
            eventKeys: a set of [[csw.params.events.EventKey]] to subscribe to
        Returns:
            a set of latest Event for the provided Event Keys
        """
        fList = list(map(lambda k: self.get(k), eventKeys))
        events: List[Event] = await asyncio.gather(*fList)
        return set(events)

    async def get(self, eventKey: EventKey) -> Event:
        """
        Get an event from the Event Service

        Args:
            eventKey (EventKey): String specifying Redis key for event.  Should be source prefix + "." + event name.

        Returns: Event obtained from Event Service, decoded into a Event
        """
        data = await self._redis.get(str(eventKey))
        if data:
            event = Event._fromDict(cbor2.loads(data))
            return event
        return SystemEvent.invalidEvent(eventKey)
