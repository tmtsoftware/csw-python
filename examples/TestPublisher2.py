from csw.Parameter import Parameter
from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.KeyType import KeyType
from csw.Units import Units
from csw.EventName import EventName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Test publishing events using the Parameter and Event wrapper classes
class TestPublisher2:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
        intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                                    Units.marcsec)
        intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        prefix = Prefix(Subsystems.CSW, "testassembly")
        eventName = EventName("myAssemblyEvent")
        event = SystemEvent(prefix, eventName, paramSet)
        self.pub.publish(event)


def main():
    TestPublisher2()


if __name__ == "__main__":
    main()
