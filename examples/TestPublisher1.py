import sys
import os
sys.path.append(os.path.relpath(".."))

from examples.TestSubscriber1 import TestSubscriber1
from csw_protobuf.keytype_pb2 import IntKey
from csw_protobuf.units_pb2 import NoUnits

import uuid

from csw_event.EventPublisher import EventPublisher
from csw_protobuf.events_pb2 import PbEvent
from csw_protobuf.parameter_pb2 import PbParameter

# Test publishing events using only the protobuf API
class TestPublisher1:

    def __init__(self):
        event = PbEvent()
        event.eventId = str(uuid.uuid4())
        event.source = "test.assembly"
        event.name = "myAssemblyEvent"
        event.eventTime.GetCurrentTime()
        event.eventType = PbEvent.SystemEvent

        parameter = PbParameter()
        parameter.name = "assemblyEventValue"
        parameter.units = NoUnits
        parameter.keyType = IntKey
        parameter.intItems.values.append(42)
        event.paramSet.extend([parameter])

        pub = EventPublisher()
        pub.publish(event)

        TestSubscriber1.callback(event)



def main():
    TestPublisher1()

if __name__ == "__main__":
    main()

