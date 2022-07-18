from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import TAITimeKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems

# Test publishing events
from csw.TAITime import TAITime

prefix = Prefix(Subsystems.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

param = TAITimeKey.make("assemblyEventValue").set(TAITime.fromSystem())
paramSet = [param]

event = SystemEvent(prefix, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
