# tmtpycsw - Python3 CSW APIs

This package contains python APIs for the [TMT Common Software (CSW)](https://github.com/tmtsoftware/csw). 

## CSW Event Service

The python API for the [CSW Event Service](https://tmtsoftware.github.io/csw/services/event.html) makes use of classes generated from protobuf definitions, which define the structure of the events that are stored in Redis. Wrapper classes were added for convenience.

## Build

Note that if you want to run the code from here (as opposed to installing it with pip), 
you will need to first [generate python code from the protobuf files](csw_protobuf/README.md).

## Installation

You can install the `tmtpycsw` package with pip3 (or pip for python3):

    pip3 install --user -i https://test.pypi.org/simple/ --upgrade tmtpycsw

### Examples 

To subscribe to an event with the key "test.assembly.myAssemblyEvent":

```python
from csw_event.EventSubscriber import EventSubscriber

class TestSubscriber:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribeSystemEvent([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        
        for i in systemEvent.paramSet:
            print(f"    with values: {i.name}: {i.items}")
        
        if (systemEvent.isInvalid()):
            print("    Invalid")
        
        if (systemEvent.exists("assemblyEventValue")):
            p = systemEvent.get("assemblyEventValue")
            if (p != None):
                print(f"Found: {p.name}")
```

To publish an event (with various types of parameters):

```python
from csw_protobuf.units_pb2 import meter, marcsec, arcsec
from csw_event.MatrixItems import IntMatrix
from csw_event.ArrayItems import IntArray, FloatArray
from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_protobuf.keytype_pb2 import IntKey, IntArrayKey, FloatArrayKey, IntMatrixKey
from csw_event.EventPublisher import EventPublisher

class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        
        intParam = Parameter("IntValue", IntKey, [42], arcsec)
        
        intArrayParam = Parameter("IntArrayValue", IntArrayKey, IntArray([[1,2,3,4], [5,6,7,8]]).items)
        
        floatArrayParam = Parameter("FloatArrayValue", FloatArrayKey, FloatArray([[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]]).items, marcsec)
        
        intMatrixParam = Parameter("IntMatrixValue", IntMatrixKey, IntMatrix([[[1,2,3,4], [5,6,7,8]],[[-1,-2,-3,-4], [-5,-6,-7,-8]]]).items, meter)
        
        event = SystemEvent("test.assembly", "myAssemblyEvent", [intParam, intArrayParam, floatArrayParam, intMatrixParam])
        self.pub.publishSystemEvent(event)
```
