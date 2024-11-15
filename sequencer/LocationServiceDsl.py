from typing import List

from csw.LocationService import LocationService, Registration, RegistrationResult, ConnectionInfo, Location, \
    ComponentType


class LocationServiceDsl:
    def __init__(self):
        super(LocationServiceDsl, self).__init__()
        self.locationService = LocationService()

    def register(self, registration: Registration) -> RegistrationResult:
        """
        Registers registration details

        Args:
            registration holds a connection, and it's corresponding location information

        Returns:
            RegistrationResult which contains registered location and handle for un-registration
        """
        return self.locationService.register(registration)

    def unregister(self, connection: ConnectionInfo):
        """
        Unregisters the connection
        """
        self.locationService.unregister(connection)

    def findLocation(self, connection: ConnectionInfo) -> Location:
        """
        Look up for the location registered against provided connection
        """
        return self.locationService.find(connection)

    def resolveLocation(self, connection: ConnectionInfo, withinSecs: int = "5") -> Location:
        """
        Resolve the location registered against provided connection
        """
        return self.locationService.resolve(connection, withinSecs)

    def listLocations(self) -> List[Location]:
        """
        Lists all the registered locations
        """
        return self.locationService.list()

    def listLocationsBy(self, compType: ComponentType) -> List[Location]:
        """
        Lists all the registered locations matching against provided component type
        """
        return self.locationService.list(compType)

    def listLocationsByHostname(self, hostname: str) -> List[Location]:
        """
        Lists all the registered locations matching against provided host name
        """
        return self.locationService.list(hostname)

    def listLocationsByPrefix(self, prefixStartsWith: str) -> List[Location]:
        """
        Lists all the registered locations that start with the provided prefix string
        """
        return self.locationService.listByPrefix(prefixStartsWith)

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
