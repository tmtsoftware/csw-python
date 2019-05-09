from csw_event.RedisConnector import RedisConnector
from csw_event.SystemEvent import SystemEvent
from cbor2 import *


class EventSubscriber:

    def __init__(self):
        self.__redis = RedisConnector()

    @staticmethod
    def __handle_callback(message, callback):
        data = message['data']
        ar = loads(data)
        cls = ar[0]
        obj = ar[1]
        if cls == 'SystemEvent':
            event = SystemEvent.deserialize(obj)
            callback(event)
            # TODO: Handle ObserveEvents
        else:
            raise Exception("Expected a SystemEvent, but got: " + cls)

    def subscribe(self, event_key_list, callback):
        """
        Start a subscription to system events in event service, specifying a callback
        to be called when an event in the list has its value updated.

        :param list event_key_list: list of event key (Strings) to subscribe to
        :param callback: function to be called when event updates. Should take SystemEvent and return void
        :return: subscription thread.  use .stop() method to stop subscription
        """
        return self.__redis.subscribeCallback(event_key_list, lambda message: self.__handle_callback(message, callback))

    def get(self, event_key):
        """
        Get an event from the Event Service

        :param event_key: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :return: Event obtained from Event Service, decoded into a SystemEvent
        """
        data = self.__redis.get(event_key)
        ar = loads(data)
        cls = ar[0]
        obj = ar[1]
        if cls == 'SystemEvent':
            event = SystemEvent.deserialize(obj)
            return event
        # TODO: Handle ObserveEvents
        else:
            raise Exception("Expected a SystemEvent, but got: " + cls)
