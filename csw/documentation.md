## Introduction

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw),
including the
[Location Service](https://tmtsoftware.github.io/csw/services/location.html),
[Event Service](https://tmtsoftware.github.io/csw/services/event.html) and
[Command Service](https://tmtsoftware.github.io/csw/commons/command.html) (receiving end only at this point).

See [here](https://tmtsoftware.github.io/csw/index.html) for the CSW documentation.

You can find the [tmtpycsw sources](https://github.com/tmtsoftware/pycsw) on GitHub.

Note that all APIs here assume that the CSW services (version 3.0.1) are running 
For example, during development, run: `csw-services start`.

The Python APIs mirror the CSW Scala and Java APIs. The classes usually have the same fields,
with the difference that in some cases the Python types are simpler, due to less strict typing.
This means that you can in general refer to the CSW Scala and Java documentation, if something is
not clear.

## Requirements

* Python version 3.8.5 or newer
* pdoc3 (`pip3 install pdoc3`)

### Python Dependencies:

The following Python dependencies need to be installed with pip (pip3):

* astropy
* cbor2
* redis
* requests
* openpyxl
* multipledispatch
* aiohttp
* dataclasses-json

For running the tests:

* pytest
* termcolor

The latest release has been published to https://pypi.org/project/tmtpycsw/ and can be installed with:

    pip3 install tmtpycsw


## CSW Location Service

The Location Service can be used to register, list and lookup CSW services.
Python applications can access `tcp` and `http` based services, but not `akka` services,
which are based on akka actors.

The following code demonstrates the Python API for the Location Service:

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

See [here](Event.html) for the structure of an event. There are two types of events:

* [SystemEvent](Event.html#csw.Event.SystemEvent) - used to publish data

* [ObserveEvent](Event.html#csw.Event.ObserveEvent) - a special event published when an observation completes

In the above example, the callback expects SystemEvents. 

## Command Service API

In the current version there is no support for command service clients. 
For now it assumed that Python code will be used to implement or help implement an HCD, for example, 
but not send commands to other components. This may be added in a future version.

The [CommandServer](CommandServer.html) class lets you start an HTTP server that will accept 
CSW Setup commands to implement an assembly or HCD in Python.
By overriding the `onSetup` and `onOneway` methods of the [ComponentHandlers](ComponentHandlers.html) 
class, you can handle commands being sent from a CSW component in Python code
and return a [CommandResponse](CommandResponse.html) to the component. 
The messages are serialized using JSON (events use CBOR, since talking directly to Redis).

Below is an example command server that accepts different types of commands.
Note that a *long running command* should do the work in another thread and
return the [CommandResponse](CommandResponse.html) later, while a *simple command* 
returns the command response immediately, possibly with a [Result](CommandResponse.html#csw.CommandResponse.Result).
If an error occurs, [Error](CommandResponse.html#csw.CommandResponse.Error) should be returned.
If the command is invalid , the server should return [Invalid](CommandResponse.html#csw.CommandResponse.Invalid)

```python
import sys
import os
import asyncio
import traceback
from asyncio import Task
from typing import List

from aiohttp.web_runner import GracefulExit
from astropy.coordinates import Angle
from termcolor import colored

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.Coords import ProperMotion, EqCoord
from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import Parameter


class MyComponentHandlers(ComponentHandlers):
    prefix = "CSW.pycswTest"
    commandServer: CommandServer = None

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(3)
        print("Long running task completed")
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        return Completed(runId)

    def _checkCommand(self, command: ControlCommand):
        try:
            assert(command.get("cmdValue").values == [1.0, 2.0, 3.0])
            assert(list(command.get("cmdValue").values)[0] == 1.0)

            # Access a coordinate value
            eqCoord: EqCoord = list(command.get("BasePosition").values)[0]
            assert(eqCoord.pm == ProperMotion(0.5, 2.33))
            assert(eqCoord.ra == Angle("12:13:14.15 hours"))
            assert(eqCoord.dec == Angle("-30:31:32.3 deg"))

        except:
            print(f"_checkCommand: {colored('TEST FAILED', 'red')}")
            traceback.print_exc()

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        self._checkCommand(command)
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")

        if command.commandName == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId, "Long running task in progress..."), task
        elif command.commandName == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName == "ResultCommand":
            result = Result([Parameter("myValue", 'DoubleKey', [42.0])])
            return Completed(runId, result), None
        elif command.commandName == "ErrorCommand":
            return Error(runId, "Error command received"), None
        elif command.commandName == "InvalidCommand":
            return Invalid(runId, MissingKeyIssue("Missing required key XXX")), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params.\n{colored('TEST PASSED', 'green')}.")
        raise GracefulExit()

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        return Accepted(runId)

    # Returns the current state
    def currentStates(self) -> List[CurrentState]:
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")
        return [CurrentState(self.prefix, "PyCswState", [intParam, intArrayParam, floatArrayParam, intMatrixParam])]

def test_command_server():
    handlers = MyComponentHandlers()
    commandServer = CommandServer(handlers.prefix, handlers)
    handlers.commandServer = commandServer
    commandServer.start()
```

## Working with Parameters

When receiving events or handling commands, you need to be able to unpack the [parameter](Parameter.html) list.
This package provides wrappers for all of the CSW parameter classes.

Normally you should know what parameters to expect, based on the ICD or by looking at the sender's code.
For example, assuming you know that a received command contains a key named "cmdValue" with the key type `FloatKey`,
you can access the values like this (Parameters may always contain multiple values):

```python
            assert(command.get("cmdValue").values == [1.0, 2.0, 3.0])
            assert(list(command.get("cmdValue").values)[0] == 1.0)
```

CSW also defines a number of 
[coordinate types](https://tmtsoftware.github.io/csw/params/keys-parameters.html#coordinate-types) for parameters.
The following example gets the first value of the "BasePosition", which is expected to be an 
[EqCoord](Coords.html#csw.Coords.EqCoord). The ra and dec fields are represented in Python as
[Astropy Angles](https://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html).

```python

            # Access a coordinate value
            eqCoord: EqCoord = list(command.get("BasePosition").values)[0]
            assert(eqCoord.pm == ProperMotion(0.5, 2.33))
            assert(eqCoord.ra == Angle("12:13:14.15 hours"))
            assert(eqCoord.dec == Angle("-30:31:32.3 deg"))
```
