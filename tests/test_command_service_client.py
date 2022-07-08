
# Assumes csw-services and test assembly are running!
from csw.CommandResponse import Completed, Accepted
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
    param = Parameter("testValue", KeyType.IntKey, [42])
    paramSet = [param]
    setup = Setup(prefix, commandName, maybeObsId, paramSet)
    resp = cs.submit(setup)
    assert isinstance(resp, Completed)
    resp2 = cs.validate(setup)
    assert isinstance(resp2, Accepted)
    resp3 = cs.oneway(setup)
    assert isinstance(resp3, Accepted)


