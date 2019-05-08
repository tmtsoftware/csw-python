import redis


class RedisConnector:

    def __init__(self):
        self.__redis = redis.Redis(
            host='localhost',
            port=6379)
        self.__redis_pubsub = self.__redis.pubsub()

    def close(self):
        self.__redis_pubsub.close()

    def subscribeCallback(self, event_key_list, callback):
        """
        Set up a Redis subscription on specified keys with specified callback on value changes.

        :param event_key_list:
        :param callback: callback called when item changes.  Should take a Redis message type.
        :return: subscription thread.  use .stop() method to stop subscription
        """
        d = dict.fromkeys(event_key_list, callback)
        self.__redis_pubsub.subscribe(**d)
        return self.__redis_pubsub.run_in_thread(sleep_time=0.001)

    def publish(self, event_key, encoded_event):
        """
        Publish CBOR encoded event string to Redis

        :param event_key: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :param encoded_event: CBOR encoded value for the event (in the form [className, dict])
        :return: None
        """
        self.__redis.set(event_key, encoded_event)
        self.__redis.publish(event_key, encoded_event)

    def get(self, event_key):
        """
        Get value from Redis using specified key

        :param event_key: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :return: Raw Redis string for event, typically in protocol buffer encoding
        """
        return self.__redis.get(event_key)
