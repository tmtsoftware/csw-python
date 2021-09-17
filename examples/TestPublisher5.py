from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.KeyType import KeyType

# Test publishing events
from csw.TAITime import TAITime

source = "CSW.testassembly"
eventName = "myAssemblyEvent"

keyName = "assemblyEventValue"
keyType = KeyType.TAITimeKey
param = Parameter(keyName, keyType, [TAITime.fromSystem()])
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
