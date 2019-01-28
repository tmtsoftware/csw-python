import uuid

from csw_event.Parameter import Parameter
from csw_protobuf.events_pb2 import PbEvent

class SystemEvent:

    def __init__(self, source, eventName, paramSet):
        """
        Creates a SystemEvent.

        :param str source: prefix representing source of the event
        :param str eventName: the name of event
        :param list paramSet: list of parameters (keys with values)
        """

        self.source = source
        self.eventName = eventName
        self.paramSet = paramSet
        event = PbEvent()
        event.eventId = str(uuid.uuid4())
        event.source = source
        event.name = eventName
        event.eventTime.GetCurrentTime()
        event.eventType = PbEvent.SystemEvent
        parameters = [p.pbParameter for p in paramSet]
        event.paramSet.extend(parameters)
        self.pbEvent = event

    @staticmethod
    def fromPbEvent(e):
        """
        Returns a SystemEvent for the given PbEvent.
        """
        i = e.paramSet
        paramSet = [Parameter.fromPbParameter(p) for p in e.paramSet]
        return SystemEvent(e.source, e.name, paramSet)
