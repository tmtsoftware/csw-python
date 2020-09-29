import cbor2

from csw.RedisConnector import RedisConnector
from csw.Event import Event


class EventSubscriber:

    def __init__(self):
        self.__redis = RedisConnector()

    @staticmethod
    def __handleCallback(message: dict, callback):
        data = message['data']
        event = Event._fromDict(cbor2.loads(data))
        callback(event)

    def subscribe(self, eventKeyList: list, callback):
        """
        Start a subscription to system events in event service, specifying a callback
        to be called when an event in the list has its value updated.

        Args:
            eventKeyList (list): list of event key (Strings) to subscribe to
            callback (function): function to be called when event updates. Should take Event and return void

        Returns: PubSubWorkerThread
            subscription thread. Use .stop() method to stop subscription.
        """
        return self.__redis.subscribe(eventKeyList, lambda message: self.__handleCallback(message, callback))

    def unsubscribe(self, eventKeyList: list):
        """
        Unsubscribes to the given list of event keys (or all keys, if eventKeyList is empty)

        Args:
            eventKeyList (list): list of event key (Strings) to unsubscribe from
        """
        return self.__redis.unsubscribe(eventKeyList)

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
    #     return self.__redis.pSubscribe(eventKeyList, lambda message: self.__handleCallback(message, callback))

    # def pUnsubscribe(self, eventKeyList: list):
    #     """
    #     Unsubscribes to the given list of event key patterns (or all keys, if eventKeyList is empty)
    #
    #     Args:
    #         eventKeyList (list): list of event key patterns (Strings) to unsubscribe from
    #     """
    #     return self.__redis.pUnsubscribe(eventKeyList)

    def get(self, eventKey: str):
        """
        Get an event from the Event Service

        Args:
            eventKey (str): String specifying Redis key for event.  Should be source prefix + "." + event name.

        Returns: Event
            Event obtained from Event Service, decoded into a Event
        """
        data = self.__redis.get(eventKey)
        event = Event._fromDict(cbor2.loads(data))
        return event
