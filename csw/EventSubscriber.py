import cbor2

from csw.RedisConnector import RedisConnector
from csw.Event import Event
#from csw.LocationService import LocationService, ComponentType, ConnectionType
#from urllib.parse import urlparse


class EventSubscriber:

    def __init__(self):
        # loc = LocationService().find("EventServer", ComponentType.Service, ConnectionType.TcpType)
        # uri = urlparse(loc.uri)
        # self.__redis = RedisConnector(host=uri.hostname, port=uri.port)
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
