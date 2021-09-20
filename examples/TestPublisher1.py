from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher
from csw.KeyType import KeyType
from csw.Parameter import Parameter
from csw.EventName import EventName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems

# Test publishing events
source = Prefix(Subsystems.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

keyName = "assemblyEventValue"
keyType = KeyType.DoubleKey
values = [42.0]
param = Parameter(keyName, keyType, values)
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
