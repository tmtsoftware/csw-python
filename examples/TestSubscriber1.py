from csw.Event import Event
from csw.EventSubscriber import EventSubscriber

# Test subscribing to events
class TestSubscriber1:

    def __init__(self):
        self.count = 0
        self.eventKey = "CSW.testassembly.myAssemblyEvent"
        self.eventSubscriber = EventSubscriber()
        self.eventThread = self.eventSubscriber.subscribe([self.eventKey], self.callback)

    def callback(self, event: Event):
        print(f"Event = {event} (Event Time = {event.eventTime.str()}")
        self.count = self.count + 1
        if (self.count > 4):
            self.eventSubscriber.unsubscribe([self.eventKey])
            self.eventThread.stop()



def main():
    TestSubscriber1()

if __name__ == "__main__":
    main()

