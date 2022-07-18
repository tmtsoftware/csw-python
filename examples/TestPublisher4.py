from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import UTCTimeKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems

# Test publishing events
from csw.UTCTime import UTCTime

prefix = Prefix(Subsystems.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

param = UTCTimeKey.make("assemblyEventValue").set(UTCTime.fromSystem())
paramSet = [param]
event = SystemEvent(prefix, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
