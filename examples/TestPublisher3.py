from csw_event.Parameter import Parameter
from csw_event.SystemEvent import SystemEvent
from csw_event.EventPublisher import EventPublisher


# Test publishing events
class TestPublisher3:
    pub = EventPublisher()

    def __init__(self):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        event = SystemEvent("test.assembly", "myAssemblyEvent", paramSet)
        self.pub.publish(event)


def main():
    TestPublisher3()


if __name__ == "__main__":
    main()
