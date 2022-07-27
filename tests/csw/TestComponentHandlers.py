import asyncio
from asyncio import Task
import pathlib
from aiohttp.web_runner import GracefulExit
from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import ComponentHandlers, CommandServer
from csw.ParameterSetType import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import *
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# noinspection DuplicatedCode
# This is a local command service used with the @pytest.fixture annotation for testing.
# See ./test_command_service_client_server.py.
class TestComponentHandlers(ComponentHandlers):
    prefix = Prefix(Subsystems.CSW, "pycswTest2")
    dir = pathlib.Path(__file__).parent.absolute()

    # noinspection PyUnusedLocal
    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(1)
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        self.log.debug("Long running task completed")
        return Completed(runId)

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component.
        See
        ./testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#makeTestCommand
        for the contents of the command's parameters.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: (CommandResponse, Task)
            a pair: (subclass of CommandResponse, Task), where the task can be None if the command response is final.
            For long-running commands, you can respond with Started(runId, "...") and a task that completes the
            work in the background.
        """
        n = len(command.paramSet)
        self.log.debug(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        if command.commandName.name == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId), task
        elif command.commandName.name == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName.name == "ResultCommand":
            result = Result([DoubleKey.make("myValue").set(42.0)])
            return Completed(runId, result), None
        elif command.commandName.name == "ErrorCommand":
            return Error(runId, "Error command received"), None
        elif command.commandName.name == "InvalidCommand":
            return Invalid(runId, MissingKeyIssue("Missing required key XXX")), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName.name}")), None

    def onOneway(self, runId: str, command: ControlCommand):
        """
        Overrides the base class onOneway method to handle commands from a CSW component.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        n = len(command.paramSet)
        self.log.debug(f"MyComponentHandlers Received oneway {str(command)} with {n} params.")
        raise GracefulExit()

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        return Accepted(runId)

    # Returns the current state
    # noinspection DuplicatedCode
    def currentStates(self) -> List[CurrentState]:
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue").set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        utcTimeParam = UTCTimeKey.make("UTCTimeValue").set(UTCTime.from_str("2021-09-17T09:17:08.608242344Z"))
        taiTimeParam = TAITimeKey.make("TAITimeValue").set(TAITime.from_str("2021-09-17T09:17:45.610701219Z"))
        params = [intParam, intArrayParam, floatArrayParam, intMatrixParam, utcTimeParam, taiTimeParam]
        return [CurrentState(self.prefix, "PyCswState", params)]


# Start a local python based command service
handlers = TestComponentHandlers()
commandServer = CommandServer(handlers.prefix, handlers)
try:
    asyncio.set_event_loop(asyncio.new_event_loop())
    commandServer.start()
except GracefulExit:
    pass
