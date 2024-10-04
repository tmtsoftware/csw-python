from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import TAITimeKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

# Test publishing events
from csw.TAITime import TAITime

prefix = Prefix(Subsystem.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

param = TAITimeKey.make("assemblyEventValue").set(TAITime.now())
paramSet = [param]

event = SystemEvent(prefix, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
