from csw.Event import Event
from csw.EventSubscriber import EventSubscriber
from csw.Subsystem import Subsystems
from csw.Prefix import Prefix
from csw.EventName import EventName
from csw.EventKey import EventKey


# Test subscribing to events
class TestSubscriber1:

    def __init__(self):
        self.count = 0
        self.eventKey = EventKey(Prefix(Subsystems.CSW, "testassembly"), EventName("myAssemblyEvent"))
        self.eventSubscriber = EventSubscriber()
        self.eventThread = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, event: Event):
        print(f"Event = {event} (Event Time = {str(event.eventTime)}")
        self.count = self.count + 1
        if (self.count > 4):
            self.eventSubscriber.unsubscribe([self.eventKey])
            self.eventThread.stop()


def main():
    TestSubscriber1()


if __name__ == "__main__":
    main()
