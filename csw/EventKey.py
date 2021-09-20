from dataclasses import dataclass

from csw.Prefix import Prefix
from csw.Event import EventName

@dataclass
class EventKey:
    """
    A wrapper class representing the key for an event

    Args:
        source (Prefix): represents the prefix of the component that publishes this event
        eventName (EventName): represents the name of the event
    """
    source: Prefix
    eventName: EventName

    def __str__(self):
        return f"{str(self.source)}.{self.eventName.name}"

    @classmethod
    def from_str(class_object, eventKeyStr: str):
        i = eventKeyStr.rindex('.')
        return EventKey(Prefix.from_str(eventKeyStr[:i]), EventName(eventKeyStr[i+1:]))
