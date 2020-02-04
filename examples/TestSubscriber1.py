from csw.EventSubscriber import EventSubscriber

# Test subscribing to events
class TestSubscriber1:

    def __init__(self):
        eventKey = "CSW.testassembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(event):
        print(f"Event value = {event.paramSet[0].values[0]}")

def main():
    TestSubscriber1()

if __name__ == "__main__":
    main()

