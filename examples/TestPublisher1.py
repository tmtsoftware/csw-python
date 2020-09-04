from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter

# Test publishing events
source = "CSW.testassembly"
eventName = "myAssemblyEvent"

keyName = "assemblyEventValue"
keyType = 'DoubleKey'
values = [42.0]
param = Parameter(keyName, keyType, values)
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
