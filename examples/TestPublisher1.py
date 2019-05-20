from csw.Event import Event
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter


# Test publishing events
class TestPublisher1:

    def __init__(self):
        source = "test.assembly"
        eventName = "myAssemblyEvent"

        keyName = "assemblyEventValue"
        keyType = 'DoubleKey'
        items = [42.0]
        param = Parameter(keyName, keyType, items)
        paramSet = [param]

        event = Event(source, eventName, paramSet)
        pub = EventPublisher()
        pub.publish(event)


def main():
    TestPublisher1()


if __name__ == "__main__":
    main()
