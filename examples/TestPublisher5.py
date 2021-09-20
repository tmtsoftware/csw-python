from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.Parameter import Parameter
from csw.KeyType import KeyType
from csw.EventName import EventName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems

# Test publishing events
from csw.TAITime import TAITime

prefix = Prefix(Subsystems.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

keyName = "assemblyEventValue"
keyType = KeyType.TAITimeKey
param = Parameter(keyName, keyType, [TAITime.fromSystem()])
paramSet = [param]

event = SystemEvent(prefix, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
