from csw.Subsystem import Subsystems
from csw.Prefix import Prefix


def test_prefix():
    p1 = Prefix(Subsystems.TCS, "ENCAssembly")
    p2 = Prefix.from_str("TCS.ENCAssembly")
    assert p1 == p2
    assert(str(p1) == "TCS.ENCAssembly")
    p1 = Prefix(Subsystems.TCS, "ENC.Assembly")
    p2 = Prefix.from_str("TCS.ENC.Assembly")
    assert(str(p1) == "TCS.ENC.Assembly")
    assert p1 == p2

