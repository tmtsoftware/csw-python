from csw.CommandResponse import Completed, Accepted, Started
from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Assumes csw-services and test assembly are running!
async def test_command_service_client():
    cs = CommandService(Prefix(Subsystems.CSW, "TestPublisher"), ComponentType.Assembly)
    prefix = Prefix(Subsystems.CSW, "TestClient")
    maybeObsId = []
    param = IntKey.make("testValue").set(42)
    paramSet = [param]
    setup = Setup(prefix, CommandName("Test"), maybeObsId, paramSet)
    resp = cs.submit(setup)
    assert isinstance(resp, Completed)
    resp2 = cs.validate(setup)
    assert isinstance(resp2, Accepted)
    resp3 = cs.oneway(setup)
    assert isinstance(resp3, Accepted)
    setup2 = Setup(prefix, CommandName("longRunningCommand"), maybeObsId, paramSet)

    # block calls
    resp4 = cs.submit(setup2)
    assert isinstance(resp4, Started)
    resp5 = cs.queryFinal(resp4.runId, 5)
    assert isinstance(resp5, Completed)
    resp6 = cs.submitAndWait(setup2, 5)
    assert isinstance(resp6, Completed)

    # async calls
    resp4a = cs.submit(setup2)
    assert isinstance(resp4a, Started)
    resp5a = await cs.queryFinalAsync(resp4a.runId, 5)
    assert isinstance(resp5a, Completed)
    resp6a = await cs.submitAndWaitAsync(setup2, 5)
    assert isinstance(resp6a, Completed)
