Note that all APIs here assume that the CSW services are running (Run `csw-services.sh start`).

The Python APIs mirror the CSW Scala and Java APIs. The classes usually have the same fields,
with the difference that in some cases the Python types are simpler, due to less strict typing.
This means that you can in general refer to the CSW Scala and Java documentation, if something is
not clear.

## Requirements

* Python version 3.8.2 or newer
* pdoc3 (`pip3 install pdoc3`)

### Python Dependencies:

The following Python packages need to be installed with pip (pip3):

* astropy
* cbor2
* redis
* requests
* openpyxl
* multipledispatch
* aiohttp
* dataclasses-json


The latest release has been published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip install tmtpycsw


## CSW Location Service

The Location Service can be used to register, list and lookup CSW services.

For example:

```python
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration

# Demonstrate usage of the Python Location Service API

def test_location_service():
    locationService = LocationService()

    # List all registered connections
    print("\nAll Locations:")
    for i in locationService.list():
        print("    " + str(i))

    # List the registered HCDs
    print("\nHCDs:")
    for i in locationService.list(ComponentType.HCD):
        print("    " + str(i))

    # List the registered http connections
    print("\nConnections on 192.168.178.78")
    for i in locationService.list("192.168.178.78"):
        print("    " + str(i))

    # List the registered http connections
    print("\nHTTP connections:")
    for i in locationService.list(ConnectionType.HttpType):
        print("    " + str(i))

    # Register a connection
    connection = ConnectionInfo("csw.myComp", ComponentType.Service.value, ConnectionType.HttpType.value)
    reg = HttpRegistration(connection, 8080, path="myservice/test")
    regResult = locationService.register(reg)
    print("\nRegistration result: " + str(regResult))

    # Find a connection
    location1 = locationService.find(connection)
    print("location1 = " + str(location1))

    # Resolve a connection (waiting if needed)
    location2 = locationService.resolve(connection)
    print("location2 = " + str(location2))

    # Unregister
    unregResult = locationService.unregister(connection)
    print("\nUnregister result: " + str(unregResult))
```

The type of the return value from methods that return a location is a subclass of
[Location](LocationService.html#csw.LocationService.Location).

You can find more information about the Location Service [here](https://tmtsoftware.github.io/csw/services/location.html).

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) uses CBOR to serialize and deserialize events that are stored in Redis.
Python wrapper classes were added for convenience.
You can publish events as well as subscribe to events in Python. 

For example, to subscribe to an event named `myAssemblyEvent` from `testassembly` in the CSW subsystem,
you can call `EventSubscriber().subscribe`:

```python
from csw.EventSubscriber import EventSubscriber


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        eventKey = "CSW.testassembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}' with event time: '{systemEvent.eventTime}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}({i.keyType}): {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
```

## Command Service API

The `CommandServer` class lets you start an HTTP server that will accept CSW Setup commands to implement an assembly or HCD in Python.
By overriding the `onSetup` and `onOneway` methods of the `ComponentHandlers` class, you can handle commands being sent from a CSW component in Python code
and return a CommandResponse to the component. The messages are serialized using JSON (events use CBOR, since talking directly to Redis).
See the [tests/test_commands_with_assembly.py](tests/test_commands_with_assembly.py) class for a code example.
