from csw.Event import Event
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter

# Test publishing events
source = "test.assembly"
eventName = "myAssemblyEvent"

keyName = "assemblyEventValue"
keyType = 'DoubleKey'
items = [42.0]
param = Parameter(keyName, keyType, items)
paramSet = [param]

event = Event(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
