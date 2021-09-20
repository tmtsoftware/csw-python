import structlog

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Demonstrate usage of the Python Location Service API

def test_location_service():
    log = structlog.get_logger()
    locationService = LocationService()

    # List all registered connections
    log.debug("\nAll Locations:")
    for i in locationService.list():
        log.debug("    " + str(i))

    # List the registered HCDs
    log.debug("\nHCDs:")
    for i in locationService.list(ComponentType.HCD):
        log.debug("    " + str(i))

    # List the registered http connections
    log.debug("\nConnections on 192.168.178.78")
    for i in locationService.list("192.168.178.78"):
        log.debug("    " + str(i))

    # List the registered http connections
    log.debug("\nHTTP connections:")
    for i in locationService.list(ConnectionType.HttpType):
        log.debug("    " + str(i))

    # Register a connection
    prefix = Prefix(Subsystems.CSW, "myComp")
    connection = ConnectionInfo(prefix, ComponentType.Service.value, ConnectionType.HttpType.value)
    reg = HttpRegistration(connection, 8080, path="myservice/test")
    regResult = locationService.register(reg)
    log.debug("\nRegistration result: " + str(regResult))

    # Find a connection
    location1 = locationService.find(connection)
    log.debug("location1 = " + str(location1))

    # Resolve a connection (waiting if needed)
    location2 = locationService.resolve(connection)
    log.debug("location2 = " + str(location2))

    # Unregister
    unregResult = locationService.unregister(connection)
    log.debug("\nUnregister result: " + str(unregResult))
