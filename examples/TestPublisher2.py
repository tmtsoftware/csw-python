from csw.Parameter import Parameter, IntKey, IntArrayKey, FloatArrayKey, IntMatrixKey
from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.KeyType import KeyType
from csw.Units import Units
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Test publishing events using the Parameter and Event wrapper classes
class TestPublisher2:
    pub = EventPublisher()

    def __init__(self):
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue").set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        prefix = Prefix(Subsystems.CSW, "testassembly")
        eventName = EventName("myAssemblyEvent")
        event = SystemEvent(prefix, eventName, paramSet)
        self.pub.publish(event)


def main():
    TestPublisher2()


if __name__ == "__main__":
    main()
