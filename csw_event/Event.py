import uuid
from dataclasses import dataclass
from typing import List
from cbor2 import *

from csw_event.Parameter import Parameter
from csw_event.EventTime import EventTime


@dataclass(frozen=True)
class Event:
    """
    Creates a Event.

    Args
        source (str): prefix representing source of the event
        eventName (str): the name of event
        paramSet (list): list of Parameter (keys with values)
        eventTime (EventTime): the time the event was created (defaults to current time)
        eventId (str): event id (optional: Should leave empty unless received from event service)
        eventType (str): CSW event class: one of "SystemEvent", "ObserveEvent" (default: "SystemEvent")
    """
    source: str
    eventName: str
    paramSet: List[Parameter]
    eventTime: EventTime = EventTime.fromSystem()
    eventId: str = str(uuid.uuid4())
    eventType: str = "SystemEvent"

    @staticmethod
    def deserialize(data):
        """
        Returns a Event for the given CBOR object.
        """
        m = loads(data)
        eventType = next(iter(m))
        assert(eventType in {"SystemEvent", "ObserveEvent"})
        obj = m[eventType]
        paramSet = list(map(lambda p: Parameter.deserialize(p), obj['paramSet']))
        eventTime = EventTime.deserialize(obj['eventTime'])
        return Event(obj['source'], obj['eventName'], paramSet, eventTime, obj['eventId'], eventType)

    def serialize(self):
        """
        :return: serialized value to be encoded to CBOR
        """
        return {self.eventType: {
            'eventId': self.eventId,
            'source': self.source,
            'eventName': self.eventName,
            'eventTime': self.eventTime.serialize(),
            'paramSet': list(map(lambda p: p.serialize(), self.paramSet))
        }}

    def isInvalid(self):
        return self.eventId == "-1"

    def get(self, keyName):
        """
        Gets the parameter with the given name, or else returns None
        :param str keyName: parameter name
        :return: the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return p

    def exists(self, keyName):
        """
        Returns true if the parameter with the given name is present in the event
        :param str keyName: parameter name
        :return: true if the parameter is found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return True
        return False
