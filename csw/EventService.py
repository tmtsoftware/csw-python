from fileinput import close

from aiohttp import ClientSession

from csw.EventPublisher import EventPublisher
from csw.EventSubscriber import EventSubscriber


class EventService:
    """
    An interface to provide access to EventPublisher and EventSubscriber.
    """

    def __init__(self):
        self._defaultPublisher = None
        self._defaultSubscriber = None

    async def defaultPublisher(self, clientSession: ClientSession) -> EventPublisher:
        """
        A default instance of EventPublisher.
        This could be shared across under normal operating conditions to share the underlying connection to event server.
        """
        if self._defaultPublisher is None:
            self._defaultPublisher = await self.makeNewPublisher(clientSession)
        return self._defaultPublisher

    async def defaultSubscriber(self, clientSession: ClientSession) -> EventSubscriber:
        """
        A default instance of EventSubscriber.
        This could be shared across under normal operating conditions to share the underlying connection to event server.
        """
        if self._defaultSubscriber is None:
            self._defaultSubscriber = await self.makeNewSubscriber(clientSession)
        return self._defaultSubscriber

    async def makeNewPublisher(self, clientSession: ClientSession) -> EventPublisher:
        """
        Create a new instance of EventPublisher with a separate underlying connection than the default instance.
        The new instance will be required when the location of Event Service is updated or in case the performance requirements
        of a publish operation demands a separate connection to be used.
        """
        return await EventPublisher.make(clientSession)

    async def makeNewSubscriber(self, clientSession: ClientSession) -> EventSubscriber:
        """
        Create a new instance of EventSubscriber with a separate underlying connection than the default instance.
        The new instance will be required when the location of Event Service is updated or in case the performance requirements
        of a subscribe operation demands a separate connection to be used.
        """
        return await EventSubscriber.make(clientSession)
