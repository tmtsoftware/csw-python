import cbor2

from csw.Event import Event
from csw.RedisConnector import RedisConnector
#from csw.LocationService import LocationService, ComponentType, ConnectionType
#from urllib.parse import urlparse


class EventPublisher:

    def __init__(self):
        # loc = LocationService().find("EventServer", ComponentType.Service, ConnectionType.TcpType)
        # uri = urlparse(loc.uri)
        # self.__redis = RedisConnector(host=uri.hostname, port=uri.port)
        self.__redis = RedisConnector()

    def publish(self, event: Event):
        """
        Publish an event to the Event Service

        :param Event event: Event to be published
        :return: None
        """
        event_key = event.source + "." + event.eventName
        obj = cbor2.dumps(event.asDict())
        self.__redis.publish(event_key, obj)
