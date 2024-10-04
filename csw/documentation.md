## Introduction

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw),
including the
[Location Service](https://tmtsoftware.github.io/csw/services/location.html),
[Event Service](https://tmtsoftware.github.io/csw/services/event.html) and
[Command Service](https://tmtsoftware.github.io/csw/commons/command.html).
[Config Service](https://tmtsoftware.github.io/csw/services/config.html).

See [here](https://tmtsoftware.github.io/csw/index.html) for the CSW documentation.

You can find the [tmtpycsw sources](https://github.com/tmtsoftware/csw-python) on GitHub.

Note that all APIs here assume that the latest version of CSW services are running 
For example, during development, run: `csw-services start`.

The Python APIs mirror the CSW Scala and Java APIs. The classes usually have the same fields,
with the difference that in some cases the Python types are simpler, due to less strict typing.

## CSW Location Service

The Location Service can be used to register, list and lookup CSW services.
Python applications can access `tcp` and `http` based services, but not `pekko` services,
which are based on pekko actors.

The following code demonstrates the Python API for the Location Service:

```python
import structlog

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


# Demonstrate usage of the Python Location Service API

def test_location_service():
    log = structlog.get_logger()
    locationService = LocationService()

    # List all registered connections
    log.debug("\nAll Locations:")
    allLocations = locationService.list()
    for i in allLocations:
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
    httpServices = locationService.list(ConnectionType.HttpType)
    for i in httpServices:
        log.debug("    " + str(i))
    assert not [x for x in httpServices if
                x.connection.prefix == 'CSW.EventServer' and x.connection.componentType == 'Service']

    # Register a connection
    prefix = Prefix(Subsystem.CSW, "myComp")
    connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
    reg = HttpRegistration(connection, LocationService.getFreePort(), path="myservice/test")
    regResult = locationService.register(reg)
    log.debug("\nRegistration result: " + str(regResult))
    assert regResult.componentType == ComponentType.Service.value
    assert regResult.prefix == 'CSW.myComp'
    assert regResult.connectionType == ConnectionType.HttpType.value

    # Find a connection
    location1 = locationService.find(connection)
    log.debug("location1 = " + str(location1))
    assert location1.connection.componentType == ComponentType.Service.value
    assert location1.connection.prefix == 'CSW.myComp'
    assert location1.connection.connectionType == ConnectionType.HttpType.value

    # Resolve a connection (waiting if needed)
    location2 = locationService.resolve(connection)
    log.debug("location2 = " + str(location2))
    assert location1 == location2

    # Unregister
    unregResult = locationService.unregister(connection)
    log.debug("\nUnregister result: " + str(unregResult))

    assert not locationService.find(connection)
```

The type of the return value from methods that return a location is a subclass of
[Location](LocationService.html#csw.LocationService.Location).

You can find more information about the Location Service in the 
 [API docs](LocationService.html#csw.LocationService.LocationService) 
and the [CSW Location Service docs](https://tmtsoftware.github.io/csw/services/location.html).

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) 
uses CBOR to serialize and deserialize events that are stored in Redis.
[Python wrapper classes](Event.html) were added for convenience.
You can [publish](EventPublisher.html) events as well as [subscribe](EventSubscriber.html) to events in Python. 

For example, to subscribe to an event named `myAssemblyEvent` from `testassembly` in the CSW subsystem,
you can call `EventSubscriber().subscribe`:

```python
from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystem
from csw.Prefix import Prefix
from csw.Event import EventName
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        self.eventKey = EventKey(Prefix(Subsystem.CSW, "testassembly"), EventName("myAssemblyEvent"))
        EventSubscriber().subscribe([self.eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName.name}' with event time: '{systemEvent.eventTime}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}({i.keyType.name}): {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
```

See [here](Event.html) for the structure of an event. There are two types of events:

* [SystemEvent](Event.html#csw.Event.SystemEvent) - used to publish data

* [ObserveEvent](Event.html#csw.Event.ObserveEvent) - a special event published when an observation completes

In the above example, the callback expects SystemEvents. 

## Command Service Client API

The [CommandService](CommandService.html) class provides a client API for sending commands to an 
assembly or HCD.

```python
from csw.CommandResponse import Completed, Accepted
from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


# Assumes csw-services and test assembly are running!
def test_command_service_client():
    cs = CommandService(Prefix(Subsystem.CSW, "TestPublisher"), ComponentType.Assembly)
    prefix = Prefix(Subsystem.CSW, "TestClient")
    commandName = CommandName("Test")
    maybeObsId = []
    param = IntKey.make("testValue").set(42)
    paramSet = [param]
    setup = Setup(prefix, commandName, maybeObsId, paramSet)
    resp = cs.submit(setup)
    assert isinstance(resp, Completed)
    resp2 = cs.validate(setup)
    assert isinstance(resp2, Accepted)
    resp3 = cs.oneway(setup)
    assert isinstance(resp3, Accepted)
```

### Subscribing to CurrentState

You can subscribe to the CurrentState of an Assembly or HCD like this:

```
    def _currentStateHandler(self, cs: CurrentState):
        print(f'Received CurrentState: {cs.stateName}')

    subscription = cs.subscribeCurrentState(["PyCswState"], self._currentStateHandler)
    ...
    subscription.cancel()
```

The returned `Subscription` object contains a reference to an [asyncio](https://docs.python.org/3/library/asyncio.html) task 
that reads the CurrentState web socket messages from the component. To cancel the subscription, call the `cancel()` method.

## Implementing an Assembly or HCD in Python

The [CommandServer](CommandServer.html) class lets you start an HTTP server that will accept 
CSW Setup commands to implement an assembly or HCD in Python.
By overriding the `onSetup` and `onOneway` methods of the [ComponentHandlers](ComponentHandlers.html) 
class, you can handle commands being sent from a CSW component in Python code
and return a [CommandResponse](CommandResponse.html) to the component. 
The messages are serialized using JSON (events use CBOR, since talking directly to Redis).

Below is an example command server that accepts different types of commands.
Note that a *long-running command* should do the work in another thread and
return the [CommandResponse](CommandResponse.html) later, while a *simple command* 
returns the command response immediately, possibly with a [Result](CommandResponse.html#csw.CommandResponse.Result).
If an error occurs, [Error](CommandResponse.html#csw.CommandResponse.Error) should be returned.
If the command is invalid , the server should return [Invalid](CommandResponse.html#csw.CommandResponse.Invalid)

```python
import asyncio
from asyncio import Task
from typing import List

from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ParameterSetType import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import IntKey, UTCTimeKey, TAITimeKey, IntArrayKey, FloatArrayKey, IntMatrixKey, DoubleKey
from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


class MyComponentHandlers(ComponentHandlers):
    prefix = Prefix(Subsystem.CSW, "pycswTest")

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(3)
        print("Long running task completed")
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        return Completed(runId)

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component
      
        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW
      
        Returns: (CommandResponse, Task)
            a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")

        if command.commandName.name == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId, "Long running task in progress..."), task
        elif command.commandName.name == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName.name == "ResultCommand":
            param = DoubleKey.make("myValue").set(42.0)
            result = Result([param])
            return Completed(runId, result), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName.name}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onOneway method to handle commands from a CSW component.
      
        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW
      
        Returns: CommandResponse
            an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params")
        return Accepted(runId)

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.
      
        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW
      
        Returns: CommandResponse
            an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(runId)

    # Returns the current state
    def currentStates(self) -> List[CurrentState]:
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue").set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        utcTimeParam = UTCTimeKey.make("UTCTimeValue").set(UTCTime.from_str("2021-09-17T09:17:08.608242344Z"))
        taiTimeParam = TAITimeKey.make("TAITimeValue").set(TAITime.from_str("2021-09-17T09:17:45.610701219Z"))
        params = [intParam, intArrayParam, floatArrayParam, intMatrixParam, utcTimeParam, taiTimeParam]
        return [CurrentState(self.prefix, "PyCswState", params)]


# noinspection PyTypeChecker
handlers = MyComponentHandlers()
commandServer = CommandServer(handlers.prefix, handlers)
print(f"Starting test command server on port {commandServer.port}")
commandServer.start()

```

## Working with Parameters

When receiving events or handling commands, you need to be able to unpack the [parameter](Parameter.html) list.
This package provides wrappers for all of the CSW parameter classes.

Normally you should know what parameters to expect, based on the ICD or by looking at the sender's code.
For example, assuming you know that a received command contains a key named "cmdValue" with the key type `FloatKey`,
you can access the values like this (Parameters may always contain multiple values):

```python
    # Access cmdValue using __call__ syntax
    cmdValueKey = FloatKey.make("cmdValue")
    assert (command(cmdValueKey).values == [1.0, 2.0, 3.0])
    
    # Alternative ways to access the parameter values
    assert (command.get("cmdValue", FloatKey).values == [1.0, 2.0, 3.0])
    assert (command.gets("cmdValue").values == [1.0, 2.0, 3.0])
```
Note that the first two versions use python generics that provide type hints for IDEs,
while the last version (gets()) does not.

CSW also defines a number of 
[coordinate types](https://tmtsoftware.github.io/csw/params/keys-parameters.html#coordinate-types) for parameters.
The following example gets the first value of the "BasePosition", which is expected to be an 
[EqCoord](Coords.html#csw.Coords.EqCoord). The ra and dec fields are represented in Python as
[Astropy Angles](https://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html).

```python
    # Access a coordinate value
    eqCoord = command.get("BasePosition", EqCoordKey).values[0]
    assert (eqCoord.pm == ProperMotion(0.5, 2.33))
    assert (eqCoord.ra == Angle("12:13:14.15 hours"))
    assert (eqCoord.dec == Angle("-30:31:32.3 deg"))
```

## Config Service

There is also a Python API for the [CSW Config Service](ConfigService.html):

```python
    configService = ConfigService()
    id = self.configService.create("foo", ConfigData(bytes('hello', 'utf-8')), comment="test")
    x = self.configService.getLatest('foo')
    assert (x.content.decode('utf-8') == 'hello')
```

The constructor takes an optional username and password. The default is config-admin1:config-admin1, 
which works for the development environment.

The content of the file to store in the Config Service is represented by the ConfigData class, which
has a content of type `bytes`:

```python
@dataclass
class ConfigData:
    content: bytes
```

This can be used for binary files. For text files, you can use the built-in `bytes` function to 
convert text to bytes or the `decode` function to convert bytes to text.
