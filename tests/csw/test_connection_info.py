from csw.LocationService import ConnectionInfo, ComponentType, ConnectionType
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


def test_connection_info():
    prefix = Prefix(Subsystem.CSW, "MyComp")
    info = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
    json = info.to_json()
    newInfo = ConnectionInfo.schema().loads(json)
    assert(newInfo == info)