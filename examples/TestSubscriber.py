import sys
import os
sys.path.append(os.path.relpath(".."))

from csw_event.EventSubscriber import EventSubscriber

# XXX TODO: Add wrapper class
class TestSubscriber:

    def __init__(self):
        eventKey = "test.assembly.myAssemblyEvent"
        EventSubscriber().subscribe([eventKey], self.callback)

    @staticmethod
    def callback(event):
        print(f"Event value = {event.paramSet[0].intItems.values[0]}")

        # Temp info
        print(f"event = {event}")
        print(f"XXX event type = {type(event)}")
        print(f"XXX eventTime type = {type(event.eventTime)}")
        print(f"XXX eventType type = {type(event.eventType)}")
        print(f"XXX event.paramSet type = {type(event.paramSet)}")
        p = event.paramSet[0]
        print(f"XXX p = {p}")
        print(f"XXX p type = {type(p)}")
        print(f"XXX p name = {p.name}")
        print(f"XXX p units = {p.units}")
        print(f"XXX p units type = {type(p.units)}")
        print(f"XXX p intItems = {p.intItems}")
        print(f"XXX p intItems type = {type(p.intItems)}")
        print(f"XXX p values = {p.intItems.values}")
        print(f"XXX p values type = {type(p.intItems.values)}")
        print(f"XXX p value = {p.intItems.values[0]}")


def main():
    TestSubscriber()

if __name__ == "__main__":
    main()

