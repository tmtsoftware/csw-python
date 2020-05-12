import uuid
from dataclasses import dataclass
from typing import List
from abc import abstractmethod

from csw.Parameter import Parameter
from csw.EventTime import EventTime


@dataclass
class Event:
    """
    Abstract base class that creates an Event that can be published to the event service
    (Don't use this class directly: The system expects a SystemEvent or an ObserveEvent).

    Args:
        source (str): prefix representing source of the event
        eventName (str): the name of event
        paramSet (list): list of Parameter (keys with values)
        eventTime (EventTime): the time the event was created (defaults to current time)
        eventId (str): event id (optional: Should leave empty unless received from event service)
    """
    source: str
    eventName: str
    paramSet: List[Parameter]
    eventTime: EventTime = EventTime.fromSystem()
    eventId: str = str(uuid.uuid4())

    @abstractmethod
    def eventType(self) -> str:
        """
        This is only here to make the Event class abstract.

        Returns: str
            the type of the event
        """
        pass

    @staticmethod
    def _fromDict(obj):
        """
        Returns a Event for the given dict.
        """
        typ = obj['_type']
        assert (typ in {"SystemEvent", "ObserveEvent"})
        paramSet = list(map(lambda p: Parameter._fromDict(p), obj['paramSet']))
        eventTime = EventTime._fromDict(obj['eventTime'])
        if typ == 'SystemEvent':
            return SystemEvent(obj['source'], obj['eventName'], paramSet, eventTime, obj['eventId'])
        else:
            return ObserveEvent(obj['source'], obj['eventName'], paramSet, eventTime, obj['eventId'])

    def _asDict(self):
        """
        Returns: dict
            a dictionary corresponding to this object
        """
        return {
            "_type": self.__class__.__name__,
            'eventId': self.eventId,
            'source': self.source,
            'eventName': self.eventName,
            'eventTime': self.eventTime._asDict(),
            'paramSet': list(map(lambda p: p._asDict(), self.paramSet))
        }

    def isInvalid(self):
        return self.eventId == "-1"

    def get(self, keyName: str):
        """
        Gets the parameter with the given name, or else returns None

        Args:
            keyName (str): parameter name

        Returns: Parameter|None
            the parameter, if found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return p

    def exists(self, keyName: str):
        """
        Returns true if the parameter with the given name is present in the event

        Args:
            keyName (str): parameter name

        Returns: bool
            true if the parameter is found
        """
        for p in self.paramSet:
            if p.keyName == keyName:
                return True
        return False


@dataclass
class SystemEvent(Event):
    """
    An event type for publishing changes in system data.

    Args:
        source (str): prefix representing source of the event
        eventName (str): the name of event
        paramSet (list): list of Parameter (keys with values)
        eventTime (EventTime): the time the event was created (defaults to current time)
        eventId (str): event id (optional: Should leave empty unless received from event service)

    """
    @abstractmethod
    def eventType(self) -> str:
        return "SystemEvent"


@dataclass
class ObserveEvent(Event):
    """
    An event type fired when an observation has taken place.

    Args:
        source (str): prefix representing source of the event
        eventName (str): the name of event
        paramSet (list): list of Parameter (keys with values)
        eventTime (EventTime): the time the event was created (defaults to current time)
        eventId (str): event id (optional: Should leave empty unless received from event service)

    """
    @abstractmethod
    def eventType(self) -> str:
        return "ObserveEvent"
