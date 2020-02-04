from csw.EventSubscriber import EventSubscriber


# Test subscribing to events
class TestSubscriber3:

    def __init__(self):
        eventKey = "CSW.testassembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(systemEvent):
        print(f"Received system event '{systemEvent.eventName}' with event time: '{systemEvent.eventTime}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}({i.keyType}): {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")


def main():
    TestSubscriber3()


if __name__ == "__main__":
    main()
