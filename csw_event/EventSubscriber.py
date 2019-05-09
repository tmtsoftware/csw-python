from csw_event.RedisConnector import RedisConnector
from csw_event.Event import Event
from cbor2 import *


class EventSubscriber:

    def __init__(self):
        self.__redis = RedisConnector()

    @staticmethod
    def __handle_callback(message, callback):
        data = message['data']
        event = Event.deserialize(data)
        callback(event)

    def subscribe(self, event_key_list, callback):
        """
        Start a subscription to system events in event service, specifying a callback
        to be called when an event in the list has its value updated.

        :param list event_key_list: list of event key (Strings) to subscribe to
        :param callback: function to be called when event updates. Should take Event and return void
        :return: subscription thread.  use .stop() method to stop subscription
        """
        return self.__redis.subscribeCallback(event_key_list, lambda message: self.__handle_callback(message, callback))

    def get(self, event_key):
        """
        Get an event from the Event Service

        :param event_key: String specifying Redis key for event.  Should be source prefix + "." + event name.
        :return: Event obtained from Event Service, decoded into a Event
        """
        data = self.__redis.get(event_key)
        event = Event.deserialize(data)
        return event
