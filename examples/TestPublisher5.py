from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter

# Test publishing events
from csw.TAITime import TAITime

source = "CSW.testassembly"
eventName = "myAssemblyEvent"

keyName = "assemblyEventValue"
keyType = 'TAITimeKey'
param = Parameter(keyName, keyType, [TAITime.fromSystem()])
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
