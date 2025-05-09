import asyncio
import os
import sys
from datetime import timedelta

import py
import pytest
from aiohttp import ClientSession
from xprocess import ProcessStarter
from csw.CommandResponse import Completed, Started
from csw.CommandService import CommandService
from csw.CurrentState import CurrentState
from csw.LocationService import ComponentType, ConnectionInfo, ConnectionType
from csw.LocationServiceSync import LocationServiceSync
from csw.Parameter import IntKey
from csw.ParameterSetType import CommandName, Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem


# Start a local python based command service (defined in TestComponentHandlers.py) for testing
from csw.Units import Units

@pytest.fixture(autouse=True)
def start_server(xprocess):
    # Remove any leftover reg from loc service
    locationService = LocationServiceSync()
    prefix = Prefix(Subsystem.CSW, "pycswTest2")
    connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
    locationService.unregister(connection)

    python_executable_full_path = sys.executable
    python_server_script_full_path = py.path.local(__file__).dirpath("TestComponentHandlers.py")
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

    class Starter(ProcessStarter):
        pattern = '======== Running on'
        # See https://pytest-xprocess.readthedocs.io/en/latest/starter.html
        env = {"PYTHONPATH": str(path), "PYTHONUNBUFFERED": "1"}
        terminate_on_interrupt = True
        args = [python_executable_full_path, python_server_script_full_path]

    xprocess.ensure("TestComponentHandlers", Starter)
    yield
    xprocess.getinfo("TestComponentHandlers").terminate()


@pytest.mark.asyncio
class TestCommandServiceClientServer:
    _csCount = 0
    _currentState: CurrentState = None

    async def _currentStateHandler(self, cs: CurrentState):
        print(f'Received CurrentState: {cs.stateName}')
        self._csCount = self._csCount + 1
        self._currentState = cs


    async def test_command_client_server(self):
        clientSession = ClientSession()
        # Create a python based command service client
        cs = CommandService(Prefix(Subsystem.CSW, "pycswTest2"), ComponentType.Service, clientSession)
        prefix = Prefix(Subsystem.CSW, "TestClient")
        resp = await cs.submit(Setup(prefix, CommandName("SimpleCommand")))
        assert isinstance(resp, Completed)
        resp2 = await cs.submit(Setup(prefix, CommandName("ResultCommand")))
        assert isinstance(resp2, Completed)
        assert len(resp2.result.paramSet) == 1

        # LongRunningCommand
        subscription = await cs.subscribeCurrentState(["PyCswState"], self._currentStateHandler)
        await asyncio.sleep(1)
        resp3 = await cs.submit(Setup(prefix, CommandName("LongRunningCommand")))
        assert isinstance(resp3, Started)
        resp4 = await cs.queryFinal(resp3.runId, timedelta(seconds=5))
        assert isinstance(resp4, Completed)
        resp5 = await cs.submitAndWait(Setup(prefix, CommandName("LongRunningCommand")), timedelta(seconds=5))
        assert isinstance(resp5, Completed)
        await asyncio.sleep(1)
        assert self._csCount == 4
        assert self._currentState.stateName == "PyCswState"
        assert self._currentState(IntKey.make("IntValue", Units.arcsec)).values[0] == 42
        subscription.cancel()
        await asyncio.sleep(1)
        resp5 = await cs.submitAndWait(Setup(prefix, CommandName("LongRunningCommand")), timedelta(seconds=5))
        assert isinstance(resp5, Completed)
        await asyncio.sleep(1)
        assert self._csCount == 4
        await clientSession.close()
