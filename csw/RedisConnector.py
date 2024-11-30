from urllib.parse import urlparse

from typing import List, Self

from aiohttp import ClientSession
from redis.sentinel import Sentinel

from csw.LocationService import ConnectionInfo, ComponentType, ConnectionType, LocationService, Location
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

# XXX TODO FIXME: Use redis.asyncio?
# See https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html
class RedisConnector:

    def __init__(self, loc: Location):
        """
        Events are posted to Redis. This is internal class used to access Redis.

        Args:
            loc (Location): EventServer location
        """
        # XXX TODO Check why only localhost works!
        # sentinel = Sentinel([(uri.hostname, uri.port)], socket_timeout=0.1)
        # print(f"XXX Sentinel({uri.port})")
        uri = urlparse(loc.uri)
        sentinel = Sentinel([("localhost", uri.port)], socket_timeout=0.1)
        self._redis = sentinel.master_for('eventServer', socket_timeout=0.1)
        self._redis_pubsub = self._redis.pubsub()

    @classmethod
    async def make(cls, clientSession: ClientSession) -> Self:
        prefix = Prefix(Subsystem.CSW, "EventServer")
        conn = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.TcpType)
        loc = await LocationService(clientSession).find(conn)
        return RedisConnector(loc)


    def close(self):
        self._redis_pubsub.close()

    # XXX TODO FIXME: Need redis with async callback!
    def subscribe(self, keyList: List[str], callback):
        """
        Set up a Redis subscription on specified keys with specified callback on value changes.

        Args:
            keyList (List[str]): list of keys to subscribe to
            callback (function): callback called when item changes.  Should take a Redis message type.

        Returns: PubSubWorkerThread
            subscription thread. Use .stop() method to stop subscription
        """
        d = dict.fromkeys(keyList, callback)
        self._redis_pubsub.subscribe(**d)
        return self._redis_pubsub.run_in_thread(sleep_time=0.001)

    def unsubscribe(self, keyList: List[str]):
        """
        Unsubscribe to the list of event keys

        Args:
            keyList (List[str]): list of keys to unsubscribe from
        """
        self._redis_pubsub.unsubscribe(keyList)

    # XXX Commented out due to Event Service performance concerns when using psubscribe
    # def pSubscribe(self, keyList: List[str], callback):
    #     """
    #     Set up a Redis subscription on specified keys with specified callback on value changes.
    #     In this case the keys are treated as glob-style patterns.
    #
    #     Args:
    #         keyList (List[str]): list of key patterns to subscribe to
    #         callback (function): callback called when item changes.  Should take a Redis message type.
    #
    #     Returns: PubSubWorkerThread
    #         subscription thread. Use .stop() method to stop subscription
    #     """
    #     d = dict.fromkeys(keyList, callback)
    #     self._redis_pubsub.psubscribe(**d)
    #     return self._redis_pubsub.run_in_thread(sleep_time=0.001)

    # def pUnsubscribe(self, keyList: List[str]):
    #     """
    #     Unsubscribe to the list of event key patterns
    #
    #     Args:
    #         keyList (List[str]): list of key patterns to unsubscribe from
    #     """
    #     self._redis_pubsub.punsubscribe(keyList)

    def publish(self, key: str, encodedValue: bytes):
        """
        Publish CBOR encoded event string to Redis

        Args:
            key: String specifying Redis key for event.  Should be source prefix + "." + event name.
            encodedValue: CBOR encoded value for the event (in the form [className, dict])
        """
        self._redis.set(key, encodedValue)
        self._redis.publish(key, encodedValue)

    def get(self, key: str) -> str:
        """
        Get value from Redis using specified key

        Args:
            key (str): String specifying Redis key for event.  Should be source prefix + "." + event name.

        Returns: str
            Raw Redis string for event, typically in some encoding
        """
        return self._redis.get(key)
