## Introduction

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw),
including the
[Location Service](https://tmtsoftware.github.io/csw/services/location.html),
[Event Service](https://tmtsoftware.github.io/csw/services/event.html) and
[Command Service](https://tmtsoftware.github.io/csw/commons/command.html) (receiving end only at this point).

See [here](https://tmtsoftware.github.io/csw/index.html) for the CSW documentation.

You can find the [tmtpycsw sources](https://github.com/tmtsoftware/csw-python) on GitHub.

Note that all APIs here assume that the CSW services (version 4.0.0) are running 
For example, during development, run: `csw-services start`.

The Python APIs mirror the CSW Scala and Java APIs. The classes usually have the same fields,
with the difference that in some cases the Python types are simpler, due to less strict typing.

## Requirements

* Python version 3.9.5 or newer
* pip (pip3 on Linux)
* pdoc3 (`pip3 install pdoc3`)
* pipenv (latest)

### Python Dependencies:

The following Python dependencies are required and can be installed in a local "virtual environment"
by typing:

```
make venv
```

This uses pip and pipenv to create a .venv directory containing the dependencies and python interpreter.

Dependecies:

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
import structlog

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration


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
 connection = ConnectionInfo("csw.myComp", ComponentType.Service.value, ConnectionType.HttpType.value)
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
import asyncio
from asyncio import Task
from typing import List

from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import Parameter
from csw.KeyType import KeyType
from csw.Units import Units


class MyComponentHandlers(ComponentHandlers):
 prefix = "CSW.pycswTest"

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

  if command.commandName == "LongRunningCommand":
   task = asyncio.create_task(self.longRunningCommand(runId, command))
   return Started(runId, "Long running task in progress..."), task
  elif command.commandName == "SimpleCommand":
   return Completed(runId), None
  elif command.commandName == "ResultCommand":
   result = Result([Parameter("myValue", KeyType.DoubleKey, [42.0])])
   return Completed(runId, result), None
  else:
   return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName}")), None

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
  intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
  intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
  floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                              Units.marcsec)
  intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                             [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)
  return [CurrentState(self.prefix, "PyCswState", [intParam, intArrayParam, floatArrayParam, intMatrixParam])]


# noinspection PyTypeChecker
handlers = MyComponentHandlers()
commandServer = CommandServer(handlers.prefix, handlers)
handlers.commandServer = commandServer
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
