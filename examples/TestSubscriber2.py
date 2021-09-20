from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystems
from csw.Prefix import Prefix
from csw.EventName import EventName
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber2:

    def __init__(self):
        self.eventKey = EventKey(Prefix(Subsystems.CSW, "testassembly"), EventName("myAssemblyEvent"))
        self.eventSubscriber = EventSubscriber()
        self.count = 0
        self.eventThread = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, systemEvent):
        print(f"Received system event '{systemEvent.eventName.name}'")
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
