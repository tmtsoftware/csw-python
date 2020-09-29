from urllib.parse import urlparse

import redis
from typing import List

from redis.sentinel import Sentinel

from csw.LocationService import ConnectionInfo, ComponentType, ConnectionType, LocationService


class RedisConnector:

    def __init__(self):
        """
        Events are posted to Redis. This is internal class used to access Redis.
        """
        conn = ConnectionInfo("CSW.EventServer", ComponentType.Service.value, ConnectionType.TcpType.value)
        loc = LocationService().find(conn)
        uri = urlparse(loc.uri)
        sentinel = Sentinel([(uri.hostname, uri.port)], socket_timeout=0.1)
        self.__redis = sentinel.master_for('eventServer', socket_timeout=0.1)
        self.__redis_pubsub = self.__redis.pubsub()

    def close(self):
        self.__redis_pubsub.close()

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
        self.__redis_pubsub.subscribe(**d)
        return self.__redis_pubsub.run_in_thread(sleep_time=0.001)

    def unsubscribe(self, keyList: List[str]):
        """
        Unsubscribe to the list of event keys

        Args:
            keyList (List[str]): list of keys to unsubscribe from
        """
        self.__redis_pubsub.unsubscribe(keyList)

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
    #     self.__redis_pubsub.psubscribe(**d)
    #     return self.__redis_pubsub.run_in_thread(sleep_time=0.001)

    # def pUnsubscribe(self, keyList: List[str]):
    #     """
    #     Unsubscribe to the list of event key patterns
    #
    #     Args:
    #         keyList (List[str]): list of key patterns to unsubscribe from
    #     """
    #     self.__redis_pubsub.punsubscribe(keyList)

    def publish(self, key: str, encodedValue: bytes):
        """
        Publish CBOR encoded event string to Redis

        Args:
            key: String specifying Redis key for event.  Should be source prefix + "." + event name.
            encodedValue: CBOR encoded value for the event (in the form [className, dict])
        """
        self.__redis.set(key, encodedValue)
        self.__redis.publish(key, encodedValue)

    def get(self, key: str) -> str:
        """
        Get value from Redis using specified key

        Args:
            key (str): String specifying Redis key for event.  Should be source prefix + "." + event name.

        Returns: str
            Raw Redis string for event, typically in some encoding
        """
        return self.__redis.get(key)
