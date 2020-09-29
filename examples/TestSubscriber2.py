from csw.EventSubscriber import EventSubscriber


# Test subscribing to events
class TestSubscriber2:

    def __init__(self):
        self.eventKey = "CSW.testassembly.myAssemblyEvent"
        self.eventSubscriber = EventSubscriber()
        self.count = 0
        self.eventThread = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        for i in systemEvent.paramSet:
            print(f"    with values: {i.keyName}: {i.values}")
        if systemEvent.isInvalid():
            print("    Invalid")
        if systemEvent.exists("assemblyEventValue"):
            p = systemEvent.get("assemblyEventValue")
            if p is not None:
                print(f"Found: {p.keyName}")
        self.count = self.count + 1
        if (self.count > 4):
            self.eventSubscriber.unsubscribe([self.eventKey])
            self.eventThread.stop()


def main():
    TestSubscriber2()


if __name__ == "__main__":
    main()
