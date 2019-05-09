# tmtpycsw - Python3 CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw). 

Note: Python version 3.7 or greater is required.

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) uses CBOR to serialize and deserialize events that are stored in Redis.
Wrapper classes were added for convenience.

## Installation

You can install the `tmtpycsw` package with pip3 (or pip for python3):

    pip3 install --user -i https://test.pypi.org/simple/ --upgrade tmtpycsw

### Examples 

To subscribe to an event with the key "test.assembly.myAssemblyEvent":

```python
from csw_event.EventSubscriber import EventSubscriber

# Test subscribing to events using the wrapper classes from the pip installed tmtpycsw package
class TestSubscriber:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.items}")
        if (systemEvent.isInvalid()):
            print("    Invalid")
        if (systemEvent.exists("assemblyEventValue")):
            p = systemEvent.get("assemblyEventValue")
            if (p != None):
                print(f"Found: {p.keyName}")

```

To publish an event (with various types of parameters):

```python
from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_event.EventPublisher import EventPublisher

# Test publishing events using the Parameter and SystemEvent wrapper classes from the pip installed tmtpycsw package
class TestPublisher:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1,2,3,4], [5,6,7,8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey", [[[1,2,3,4], [5,6,7,8]],[[-1,-2,-3,-4], [-5,-6,-7,-8]]], "meter")
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        event = SystemEvent("test.assembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)
```
