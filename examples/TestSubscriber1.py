import sys
import os
sys.path.append(os.path.relpath(".."))

from csw_event.EventSubscriber import EventSubscriber

# Test subscribing to events using only the protobuf API
class TestSubscriber1:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(event):
        print(f"Event value = {event.paramSet[0].intItems.values[0]}")

def main():
    TestSubscriber1()

if __name__ == "__main__":
    main()

