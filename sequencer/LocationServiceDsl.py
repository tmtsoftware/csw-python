from typing import List

from aiohttp import ClientSession

from csw.LocationService import LocationService, Registration, RegistrationResult, ConnectionInfo, Location, \
    ComponentType


class LocationServiceDsl:
    def __init__(self, clientSession: ClientSession):
        super(LocationServiceDsl, self).__init__()
        self.locationService = LocationService(clientSession)

    async def register(self, registration: Registration) -> RegistrationResult:
        """
        Registers registration details

        Args:
            registration holds a connection, and it's corresponding location information

        Returns:
            RegistrationResult which contains registered location and handle for un-registration
        """
        return await self.locationService.register(registration)

    async def unregister(self, connection: ConnectionInfo):
        """
        Unregisters the connection
        """
        await self.locationService.unregister(connection)

    async def findLocation(self, connection: ConnectionInfo) -> Location:
        """
        Look up for the location registered against provided connection
        """
        return await self.locationService.find(connection)

    async def resolveLocation(self, connection: ConnectionInfo, withinSecs: int = "5") -> Location:
        """
        Resolve the location registered against provided connection
        """
        return await self.locationService.resolve(connection, withinSecs)

    async def listLocations(self) -> List[Location]:
        """
        Lists all the registered locations
        """
        return await self.locationService.list()

    async def listLocationsBy(self, compType: ComponentType) -> List[Location]:
        """
        Lists all the registered locations matching against provided component type
        """
        return await self.locationService.list(compType)

    async def listLocationsByHostname(self, hostname: str) -> List[Location]:
        """
        Lists all the registered locations matching against provided host name
        """
        return await self.locationService.list(hostname)

    async def listLocationsByPrefix(self, prefixStartsWith: str) -> List[Location]:
        """
        Lists all the registered locations that start with the provided prefix string
        """
        return await self.locationService.listByPrefix(prefixStartsWith)

    # XXX TODO
    # /**
    #  * Subscribe to the connection and executes a callback on every location changed event
    #  *
    #  * @param connection a connection to be tracked
    #  * @param callback task which consumes [TrackingEvent] and returns [Unit]
    #  * @return an [Subscription] object which has a handle for canceling subscription
    #  */
    # fun onLocationTrackingEvent(connection: Connection, callback: SuspendableConsumer<TrackingEvent>): Subscription =
    #         locationService.subscribe(connection) { callback.toJava(it) }
    #
