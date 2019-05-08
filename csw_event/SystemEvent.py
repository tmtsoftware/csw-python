import uuid

from csw_event.Parameter import Parameter
from csw_event.EventTime import EventTime


# class Event:
#     def __init__(self, obj):
#         self.id = obj['eventId']
#         self.prefix = obj['source']
#         self.event_name = obj['eventName']
#         self.event_time = obj['eventTime']
#         self.param_set = toParameterSet(obj['paramSet'])
#
#     def __repr__(self):
#         return "id=" + self.id + "\n" + \
#                "prefix=" + self.prefix + "\n" + \
#                "name=" + self.event_name + "\n" + \
#                "time=" + str(self.event_time) + "\n" + \
#                "paramSet=" + str(self.param_set)

class SystemEvent:

    def __init__(self, source, eventName, eventTime, paramSet, eventId = str(uuid.uuid4())):
        """
        Creates a SystemEvent.

        :param str source: prefix representing source of the event
        :param str eventName: the name of event
        :param EventTime eventTime: the time the event was created
        :param list[Parameter] paramSet: list of parameters (keys with values)
        :param str eventId: event id (optional: Should leave empty unless received from event service)
        """

        self.source = source
        self.eventName = eventName
        self.eventTime = eventTime
        self.paramSet = paramSet
        self.eventId = eventId

    @staticmethod
    def fromCbor(obj):
        """
        Returns a SystemEvent for the given CBOR object.
        """
        paramSet = list(map(lambda p: Parameter.fromCbor(p), obj['paramSet']))
        eventTime = EventTime.fromCbor(obj['eventTime'])
        return SystemEvent(obj['source'], obj['eventName'], eventTime, paramSet, obj['eventId'])

    def isInvalid(self):
        return self.eventId == "-1"

    def get(self, keyName):
        """
        Gets the parameter with the given name, or else returns None
        :param str keyName: parameter name
        :return: the parameter, if found
        """
        for p in self.paramSet:
            if (p.keyName == keyName):
                return p

    def exists(self, keyName):
        """
        Returns true if the parameter with the given name is present in the event
        :param str keyName: parameter name
        :return: true if the parameter is found
        """
        for p in self.paramSet:
            if (p.keyName == keyName):
                return True
        return False
