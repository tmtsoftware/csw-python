from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Parameter import UTCTimeKey
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

# Test publishing events
from csw.UTCTime import UTCTime

prefix = Prefix(Subsystem.CSW, "testassembly")
eventName = EventName("myAssemblyEvent")

param = UTCTimeKey.make("assemblyEventValue").set(UTCTime.now())
paramSet = [param]
event = SystemEvent(prefix, eventName, paramSet)
pub = EventPublisher()
pub.publish(event)
