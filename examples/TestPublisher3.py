
from csw_protobuf.units_pb2 import meter, marcsec, arcsec
from csw_event.MatrixItems import IntMatrix
from csw_event.ArrayItems import IntArray, FloatArray
from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_protobuf.keytype_pb2 import IntKey, IntArrayKey, FloatArrayKey, IntMatrixKey
from csw_event.EventPublisher import EventPublisher

# Test publishing events using the Parameter and SystemEvent wrapper classes from the pip installed tmtpycsw package
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", IntKey, [42], arcsec)
        intArrayParam = Parameter("IntArrayValue", IntArrayKey, IntArray([[1,2,3,4], [5,6,7,8]]).items)
        floatArrayParam = Parameter("FloatArrayValue", FloatArrayKey, FloatArray([[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]]).items, marcsec)
        intMatrixParam = Parameter("IntMatrixValue", IntMatrixKey, IntMatrix([[[1,2,3,4], [5,6,7,8]],[[-1,-2,-3,-4], [-5,-6,-7,-8]]]).items, meter)
        event = SystemEvent("test.assembly", "myAssemblyEvent", [intParam, intArrayParam, floatArrayParam, intMatrixParam])
        self.pub.publishSystemEvent(event)

def main():
    TestPublisher3()

if __name__ == "__main__":
    main()

