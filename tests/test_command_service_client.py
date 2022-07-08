
# Assumes csw-services and test assembly are running!
from csw.CommandResponse import Completed
from csw.CommandService import CommandService
from csw.KeyType import KeyType
from csw.LocationService import ComponentType
from csw.Parameter import Parameter
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


def test_command_service_client():
    cs = CommandService(Prefix(Subsystems.CSW, "TestPublisher"), ComponentType.Assembly)
    prefix = Prefix(Subsystems.CSW, "TestClient")
    commandName = CommandName("Test")
    maybeObsId = []
    paramSet = []
    setup = Setup(prefix, commandName, maybeObsId, paramSet)
    resp = cs.submit(setup)
    assert isinstance(resp, Completed)
    assert resp.result.paramSet == []
    param = Parameter("testValue", KeyType.IntKey, [42])
    setup2 = Setup(prefix, commandName, maybeObsId, [param])
    resp2 = cs.submit(setup2)
    assert isinstance(resp2, Completed)
    assert resp.result.paramSet == []


