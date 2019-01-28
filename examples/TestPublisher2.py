import sys
import os

from csw_event.ItemTypes import IntArray
from csw_protobuf.parameter_types_pb2 import IntItems

sys.path.append(os.path.relpath(".."))

from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_protobuf.keytype_pb2 import IntKey, IntArrayKey

from csw_event.EventPublisher import EventPublisher

# Test publishing events using the Parameter and SystemEvent wrapper classes
class TestPublisher2:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", IntKey, [42])
        intArrayParam = Parameter("ArrayValue", IntArrayKey, IntArray([[1,2,3,4], [5,6,7,8]]).items)
        event = SystemEvent("test.assembly", "myAssemblyEvent", [intParam, intArrayParam])
        self.pub.publishSystemEvent(event)

def main():
    TestPublisher2()

if __name__ == "__main__":
    main()

