import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.Event import SystemEvent

# Simple test that publishes an event and subscribes to it
# Requires that CSW services are running.
def test_pub_sub():
    pub = EventPublisher()
    sub = EventSubscriber()

    prefix = "CSW.assembly"
    eventName = "test_event"
    eventKey = prefix + "." + eventName

    keyName = "testEventValue"
    keyType = 'IntKey'
    values = [42]
    param = Parameter(keyName, keyType, values)
    paramSet = [param]

    event = SystemEvent(prefix, eventName, paramSet)

    thread = sub.subscribe([eventKey], callback)
    pub.publish(event)
    e = sub.get(eventKey)
    try:
        assert (e == event)
    finally:
        thread.stop()

def callback(systemEvent):
    print(f"Received system event '{systemEvent.eventName}'")
    for i in systemEvent.paramSet:
        print(f"    with values: {i.keyName}: {i.values}")
    if systemEvent.isInvalid():
        print("    Invalid")
    if systemEvent.exists("testEventValue"):
        p = systemEvent.get("testEventValue")
        if p is not None:
            print(f"Found: {p.keyName}")
