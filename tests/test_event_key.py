from csw.Subsystem import Subsystems
from csw.Prefix import Prefix
from csw.EventName import EventName
from csw.EventKey import EventKey


def test_event_key():
    prefix = Prefix(Subsystems.TCS, "ENCAssembly")
    prefix2 = Prefix(Subsystems.TCS, "ENC.Assembly")
    eventName = EventName("CurrentPosition")
    k1 = EventKey(prefix, eventName)
    k2 = EventKey.from_str("TCS.ENCAssembly.CurrentPosition")
    assert k1 == k2
    k1 = EventKey(prefix2, eventName)
    k2 = EventKey.from_str("TCS.ENC.Assembly.CurrentPosition")
    assert k1 == k2
