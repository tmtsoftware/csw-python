import redis
from typing import List


class RedisConnector:
    """
    Events are posted to Redis. This is internal class used to access Redis.
    """

    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.__redis = redis.Redis(host=host, port=port)
        self.__redis_pubsub = self.__redis.pubsub()

    def close(self):
        self.__redis_pubsub.close()

    def subscribeCallback(self, eventKeyList: List[str], callback):
        """
        Set up a Redis subscription on specified keys with specified callback on value changes.

        :param eventKeyList:
        :param callback: callback called when item changes.  Should take a Redis message type.
        :return: subscription thread.  use .stop() method to stop subscription
        """
        d = dict.fromkeys(eventKeyList, callback)
        self.__redis_pubsub.subscribe(**d)
        return self.__redis_pubsub.run_in_thread(sleep_time=0.001)

    def publish(self, eventKey: str, encodedEvent: bytes):
        """
        Publish CBOR encoded event string to Redis

        :param eventKey: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :param encodedEvent: CBOR encoded value for the event (in the form [className, dict])
        :return: None
        """
        self.__redis.set(eventKey, encodedEvent)
        self.__redis.publish(eventKey, encodedEvent)

    def get(self, eventKey: str):
        """
        Get value from Redis using specified key

        :param eventKey: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :return: Raw Redis string for event, typically in protocol buffer encoding
        """
        return self.__redis.get(eventKey)
