import structlog
from aiohttp import ClientSession

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration, \
    LocationServiceUtil
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


# Demonstrate usage of the Python Location Service API

async def test_location_service():
    log = structlog.get_logger()
    clientSession = ClientSession()
    locationService = LocationService(clientSession)

    # List all registered connections
    log.debug("\nAll Locations:")
    allLocations = await locationService.list()
    for i in allLocations:
        log.debug("    " + str(i))
    # Check that the standard CSW services were found
    # assert [x for x in allLocations if x.connection.prefix == 'CSW.AAS' and x.connection.componentType == 'Service']
    # assert [x for x in allLocations if
    #         x.connection.prefix == 'CSW.AlarmServer' and x.connection.componentType == 'Service']
    # assert [x for x in allLocations if
    #         x.connection.prefix == 'CSW.DatabaseServer' and x.connection.componentType == 'Service']
    assert [x for x in allLocations if
            x.connection.prefix == 'CSW.EventServer' and x.connection.componentType == 'Service']
    # assert [x for x in allLocations if
    #         x.connection.prefix == 'CSW.ConfigServer' and x.connection.componentType == 'Service']

    # List the registered HCDs
    log.debug("\nHCDs:")
    for i in await locationService.list(ComponentType.HCD):
        log.debug("    " + str(i))

    # List the registered http connections
    log.debug("\nConnections on 192.168.178.78")
    for i in await locationService.list("192.168.178.78"):
        log.debug("    " + str(i))

    # List the registered http connections
    log.debug("\nHTTP connections:")
    httpServices = await locationService.list(ConnectionType.HttpType)
    for i in httpServices:
        log.debug("    " + str(i))
    # assert [x for x in httpServices if x.connection.prefix == 'CSW.AAS' and x.connection.componentType == 'Service']
    # assert not [x for x in httpServices if
    #             x.connection.prefix == 'CSW.AlarmServer' and x.connection.componentType == 'Service']
    # assert not [x for x in httpServices if
    #             x.connection.prefix == 'CSW.DatabaseServer' and x.connection.componentType == 'Service']
    assert not [x for x in httpServices if
                x.connection.prefix == 'CSW.EventServer' and x.connection.componentType == 'Service']
    # assert [x for x in httpServices if
    #         x.connection.prefix == 'CSW.ConfigServer' and x.connection.componentType == 'Service']

    # Register a connection
    prefix = Prefix(Subsystem.CSW, "myComp")
    connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
    reg = HttpRegistration(connection, LocationServiceUtil.getFreePort(), path="myservice/test")
    await locationService.unregister(connection)
    regResult = await locationService.register(reg)
    log.debug("\nRegistration result: " + str(regResult))
    assert regResult.location.connection.componentType == ComponentType.Service.value
    assert regResult.location.connection.prefix == 'CSW.myComp'
    assert regResult.location.connection.connectionType == ConnectionType.HttpType.value

    # Find a connection
    location1 = await locationService.find(connection)
    log.debug("location1 = " + str(location1))
    assert location1.connection.componentType == ComponentType.Service.value
    assert location1.connection.prefix == 'CSW.myComp'
    assert location1.connection.connectionType == ConnectionType.HttpType.value

    # Resolve a connection (waiting if needed)
    location2 = await locationService.resolve(connection)
    log.debug("location2 = " + str(location2))
    assert location1 == location2

    # Unregister
    unregResult = await locationService.unregister(connection)
    log.debug("\nUnregister result: " + str(unregResult))

    assert not await locationService.find(connection)
