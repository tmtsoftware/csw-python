import redis
from typing import List


class RedisConnector:

    def __init__(self, host: str = 'localhost', port: int = 6379):
        """
        Events are posted to Redis. This is internal class used to access Redis.

        Args:
            host (str): the host redis is running on (default: localhost)
            port (int): the redis port (default: 6379)
        """
        self.__redis = redis.Redis(host=host, port=port)
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
