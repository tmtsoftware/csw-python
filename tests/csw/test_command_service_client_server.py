import os
import sys
import py
import pytest
from xprocess import ProcessStarter
from csw.CommandResponse import Completed
from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.ParameterSetType import CommandName, Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# Start a local python based command service (defined in TestComponentHandlers.py) for testing
@pytest.fixture(autouse=True)
def start_server(xprocess):
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


# noinspection DuplicatedCode
def test_command_client_server():
    # Create a python based command service client
    cs = CommandService(Prefix(Subsystems.CSW, "pycswTest2"), ComponentType.Service)
    prefix = Prefix(Subsystems.CSW, "TestClient")
    maybeObsId = []
    resp = cs.submit(Setup(prefix, CommandName("SimpleCommand"), maybeObsId, []))
    assert isinstance(resp, Completed)
    resp2 = cs.submit(Setup(prefix, CommandName("ResultCommand"), maybeObsId, []))
    assert isinstance(resp2, Completed)
    assert len(resp2.result.paramSet) == 1
    print("XXX OK")