# tmtpycsw - Python3 CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw). 

Note: Python version 3.7 or greater is required.

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) uses CBOR to serialize and deserialize events that are stored in Redis.
Python wrapper classes were added for convenience.
You can publish events as well as subscribe to events in Python. See the examples directory for some code examples.

## Command Service API

The `TestCommandServer` class lets you start an HTTP server that will accept CSW Setup commands.
By overriding the `onSetup` and `onOneway` methods, you can handle commands being sent from a CSW component in Python code
and return a CommandResponse to the component. The messages are serialized using JSON (events use CBOR, since talking directly to Redis).
See the `examples/TestCommandServer` class for a code example.

## Installation

You can install the `tmtpycsw` package with pip3 (or pip for python3):

    pip3 install --user -i https://test.pypi.org/simple/ --upgrade tmtpycsw

### Examples 

To subscribe to an event with the key "test.assembly.myAssemblyEvent":

```python
from csw.EventSubscriber import EventSubscriber


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}({i.keyType}): {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
```

To publish an event (with various types of parameters):

```python
from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
from csw.Parameter import Parameter, Struct
from csw.Event import Event
from csw.EventPublisher import EventPublisher


# Test publishing events
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        floatParam = Parameter("floatValue", "FloatKey", [float(42.1)], "arcsec")
        longParam = Parameter("longValue", "LongKey", [42], "arcsec")
        shortParam = Parameter("shortValue", "ShortKey", [42], "arcsec")
        byteParam = Parameter("byteValue", "ByteKey", b'\xDE\xAD\xBE\xEF')
        booleanParam = Parameter("booleanValue", "BooleanKey", [True, False], "arcsec")

        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")
        doubleArrayParam = Parameter("DoubleArrayValue", "DoubleArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")

        byteArrayParam = Parameter("ByteArrayValue", "ByteArrayKey", [b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4])])

        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234,
                                                 "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = Parameter("CoordParam", "CoordKey",
                                [eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord, altAzCoord])

        structParam = Parameter("MyStruct", "StructKey", [Struct(
            [coordsParam, intParam, floatParam, longParam, shortParam, booleanParam, intArrayParam, floatArrayParam,
             doubleArrayParam, intMatrixParam])])

        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam, structParam]
        event = Event("test.assembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)
```

Events that you create in python are by default `SystemEvent`s. You can pass an optional `eventType` parameter to create an `ObserveEvent` instead.
Parameters are packed in a python `Parameter` class for convenience. A `Struct` class is used to hold any parameter values of type `Struct`.

Coordinate parameter angle values, such as ra and dec all expect the same syntax as astropy's Angle class.
The `make` methods are convenience factor methods, while the constructors expect actual Angle parameters.

## Command Server Example

The following example shows how to start an HTTP command server. The default port is 8082, but can be passed as a parameter to
the CommandServer class.

```python
from csw.CommandResponse import CommandResponse, CompletedWithResult, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.Parameter import Parameter


class MyComponentHandlers(ComponentHandlers):
    def onSubmit(self, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onSubmit method to handle commands from a CSW component
        :param command: contains the ControlCommand from CSW
        :return: a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        # filt = command.get("filter").values[0]
        # encoder = command.get("encoder").values[0]
        # print(f"filter = {filt}, encoder = {encoder}")

        # --- Example return values ---

        # return Completed(command.runId)

        # return Error(command.runId, "There is a problem ...")

        # return Invalid(command.runId, MissingKeyIssue("Missing required key XXX"))

        return CompletedWithResult(command.runId, Result("tcs.filter", [Parameter("myValue", 'DoubleKey', [42.0])]))

    def onOneway(self, command: ControlCommand):
        """
        Overrides the base class onOneway method to handle commands from a CSW component.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params")
        filt = command.get("filter").values[0]
        encoder = command.get("encoder").values[0]
        print(f"filter = {filt}, encoder = {encoder}")
        return Accepted(command.runId)

    def validate(self, command: ControlCommand):
        """
        Overrides the base class validate method to verify that the given command is valid.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(command.runId)

# noinspection PyTypeChecker
commandServer = CommandServer("pycswTest", MyComponentHandlers)
```