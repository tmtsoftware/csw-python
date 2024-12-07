
from csw.EventPublisher import EventPublisher
from csw.EventSubscriber import EventSubscriber


class EventService:
    """
    An interface to provide access to EventPublisher and EventSubscriber.
    """

    def __init__(self):
        self._defaultPublisher = None
        self._defaultSubscriber = None

    def defaultPublisher(self) -> EventPublisher:
        """
        A default instance of EventPublisher.
        This could be shared across under normal operating conditions to share the underlying connection to event server.
        """
        if self._defaultPublisher is None:
            self._defaultPublisher = self.makeNewPublisher()
        return self._defaultPublisher

    def defaultSubscriber(self) -> EventSubscriber:
        """
        A default instance of EventSubscriber.
        This could be shared across under normal operating conditions to share the underlying connection to event server.
        """
        if self._defaultSubscriber is None:
            self._defaultSubscriber = self.makeNewSubscriber()
        return self._defaultSubscriber

    def makeNewPublisher(self) -> EventPublisher:
        """
        Create a new instance of EventPublisher with a separate underlying connection than the default instance.
        The new instance will be required when the location of Event Service is updated or in case the performance requirements
        of a publish operation demands a separate connection to be used.
        """
        return EventPublisher.make()

    def makeNewSubscriber(self) -> EventSubscriber:
        """
        Create a new instance of EventSubscriber with a separate underlying connection than the default instance.
        The new instance will be required when the location of Event Service is updated or in case the performance requirements
        of a subscribe operation demands a separate connection to be used.
        """
        return EventSubscriber.make()
