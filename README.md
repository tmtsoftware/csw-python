# tmtpycsw - Python3 CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw). 

Note: Python version 3.7 or greater is required.

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) uses CBOR to serialize and deserialize events that are stored in Redis.
Wrapper classes were added for convenience.

Note: It is not possible to publish *Float* values from python (they always come out as Doubles), however subscribing to Float values works. 

## Installation

You can install the `tmtpycsw` package with pip3 (or pip for python3):

    pip3 install --user -i https://test.pypi.org/simple/ --upgrade tmtpycsw

### Examples 

To subscribe to an event with the key "test.assembly.myAssemblyEvent":

```python
from csw_event.EventSubscriber import EventSubscriber


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.items}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
```

To publish an event (with various types of parameters):

```python
from csw_event.Parameter import Parameter, Struct
from csw_event.Event import Event
from csw_event.EventPublisher import EventPublisher


# Test publishing events
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        doubleArrayParam = Parameter("DoubleArrayValue", "DoubleArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")

        structParam = Parameter("MyStruct", "StructKey", [Struct([intParam, intArrayParam, doubleArrayParam, intMatrixParam])])

        paramSet = [intParam, intArrayParam, doubleArrayParam, intMatrixParam, structParam]
        event = Event("test.assembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)
```

Events that you create in python are by default `SystemEvent`s. You can pass an optional `eventType` parameter to create an `ObserveEvent` instead.
Parameters are packed in a python `Parameter` class for convenience. A `Struct` class is used to hold any parameter values of type `Struct`.
