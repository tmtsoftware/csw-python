from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.KeyType import KeyType

# Test publishing events
from csw.UTCTime import UTCTime

source = "CSW.testassembly"
eventName = "myAssemblyEvent"

keyName = "assemblyEventValue"
keyType = KeyType.UTCTimeKey
values = [UTCTime.fromSystem()]
param = Parameter(keyName, keyType, values)
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
