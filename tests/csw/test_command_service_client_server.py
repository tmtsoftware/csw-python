import asyncio
import os
import sys

import py
import pytest
from xprocess import ProcessStarter
from csw.CommandResponse import Completed, Started
from csw.CommandService import CommandService
from csw.CurrentState import CurrentState
from csw.LocationService import ComponentType, LocationService, ConnectionInfo, ConnectionType
from csw.Parameter import IntKey
from csw.ParameterSetType import CommandName, Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Start a local python based command service (defined in TestComponentHandlers.py) for testing
from csw.Units import Units


@pytest.fixture(autouse=True)
def start_server(xprocess):
    # Remove any leftover reg from loc service
    locationService = LocationService()
    prefix = Prefix(Subsystems.CSW, "pycswTest2")
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


# noinspection DuplicatedCode,PyPep8Naming
class TestCommandServiceClientServer:
    _csCount = 0
    _currentState: CurrentState = None

    def _currentStateHandler(self, cs: CurrentState):
        print(f'Received CurrentState: {cs.stateName}')
        self._csCount = self._csCount + 1
        self._currentState = cs


    async def test_command_client_server(self):
        # Create a python based command service client
        cs = CommandService(Prefix(Subsystems.CSW, "pycswTest2"), ComponentType.Service)
        prefix = Prefix(Subsystems.CSW, "TestClient")
        maybeObsId = []
        resp = cs.submit(Setup(prefix, CommandName("SimpleCommand"), maybeObsId, []))
        assert isinstance(resp, Completed)
        resp2 = cs.submit(Setup(prefix, CommandName("ResultCommand"), maybeObsId, []))
        assert isinstance(resp2, Completed)
        assert len(resp2.result.paramSet) == 1

        # LongRunningCommand
        subscription = cs.subscribeCurrentState(["PyCswState"], self._currentStateHandler)
        await asyncio.sleep(1)
        resp3 = cs.submit(Setup(prefix, CommandName("LongRunningCommand"), maybeObsId, []))
        assert isinstance(resp3, Started)
        resp4 = cs.queryFinal(resp3.runId, 5)
        assert isinstance(resp4, Completed)
        resp5 = cs.submitAndWait(Setup(prefix, CommandName("LongRunningCommand"), maybeObsId, []), 5)
        assert isinstance(resp5, Completed)
        await asyncio.sleep(1)
        assert self._csCount == 4
        assert self._currentState.stateName == "PyCswState"
        assert self._currentState(IntKey.make("IntValue", Units.arcsec)).values[0] == 42
        subscription.cancel()
        await asyncio.sleep(1)
        resp5 = cs.submitAndWait(Setup(prefix, CommandName("LongRunningCommand"), maybeObsId, []), 5)
        assert isinstance(resp5, Completed)
        await asyncio.sleep(1)
        assert self._csCount == 4
        asyncio.get_event_loop().stop()
