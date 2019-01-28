import sys
import os
sys.path.append(os.path.relpath(".."))

from csw_protobuf.keytype_pb2 import IntKey
from csw_protobuf.parameter_types_pb2 import IntItems
from csw_protobuf.units_pb2 import NoUnits

import uuid

from csw_event.EventPublisher import EventPublisher
from csw_protobuf.events_pb2 import PbEvent
from csw_protobuf.parameter_pb2 import PbParameter

# XXX TODO: Add wrapper class
class TestPublisher:

    def __init__(self):
        event = PbEvent()
        event.eventId = str(uuid.uuid4())
        event.source = "test.assembly"
        event.name = "myAssemblyEvent"

        paramSet = PbParameter()
        paramSet.name = "assemblyEventValue"
        paramSet.units = NoUnits
        paramSet.keyType = IntKey
        paramSet.intItems.values.append(42)
        
        event.paramSet.extend([paramSet])

        event.eventType = PbEvent.SystemEvent

        pub = EventPublisher()
        pub.publish(event)

def main():
    TestPublisher()

if __name__ == "__main__":
    main()

