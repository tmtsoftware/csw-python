from csw.LocationService import ConnectionInfo, ComponentType, ConnectionType
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


def test_connection_info():
    prefix = Prefix(Subsystems.CSW, "MyComp")
    info = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
    json = info.to_json()
    newInfo = ConnectionInfo.schema().loads(json)
    assert(newInfo == info)