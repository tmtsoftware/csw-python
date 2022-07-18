from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import DoubleKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems

# Test publishing events
source = Prefix(Subsystems.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")
param = DoubleKey.make("assemblyEventValue").set(42.0)
paramSet = [param]

event = SystemEvent(source, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
