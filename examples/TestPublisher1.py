from csw_event.SystemEvent import SystemEvent
from csw_event.EventPublisher import EventPublisher
from csw_event.Parameter import Parameter


# Test publishing events
class TestPublisher1:

    def __init__(self):
        source = "test.assembly"
        eventName = "myAssemblyEvent"

        keyName = "assemblyEventValue"
        keyType = 'IntKey'
        items = [42]
        param = Parameter(keyName, keyType, items)
        paramSet = [param]

        event = SystemEvent(source, eventName, paramSet)
        pub = EventPublisher()
        pub.publish(event)


def main():
    TestPublisher1()


if __name__ == "__main__":
    main()
