from csw.CommandResponse import Completed, Accepted, Started
from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from aiohttp import ClientSession


# Assumes csw-services and test assembly are running!
async def test_command_service_client():
    clientSession = ClientSession()
    cs = CommandService(Prefix(Subsystem.CSW, "TestPublisher"), ComponentType.Assembly, clientSession)
    prefix = Prefix(Subsystem.CSW, "TestClient")
    maybeObsId = None
    param = IntKey.make("testValue").set(42)
    paramSet = [param]
    setup = Setup(prefix, CommandName("Test"), maybeObsId, paramSet)
    resp = await cs.submit(setup)
    assert isinstance(resp, Completed)
    resp2 = await cs.validate(setup)
    assert isinstance(resp2, Accepted)
    resp3 = await cs.oneway(setup)
    assert isinstance(resp3, Accepted)
    setup2 = Setup(prefix, CommandName("longRunningCommand"), maybeObsId, paramSet)

    resp4 = await cs.submit(setup2)
    assert isinstance(resp4, Started)
    resp5 = await cs.queryFinal(resp4.runId, 5)
    assert isinstance(resp5, Completed)
    resp6 = await cs.submitAndWait(setup2, 5)
    assert isinstance(resp6, Completed)

    resp4a = await cs.submit(setup2)
    assert isinstance(resp4a, Started)
    resp5a = await cs.queryFinalAsync(resp4a.runId, 5)
    assert isinstance(resp5a, Completed)
    resp6a = await cs.submitAndWaitAsync(setup2, 5)
    assert isinstance(resp6a, Completed)
