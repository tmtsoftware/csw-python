import filecmp
import sys
import os
import asyncio
import traceback
from asyncio import Task
from typing import List

import pathlib

import structlog
from aiohttp.web_runner import GracefulExit
from astropy.coordinates import Angle
from termcolor import colored

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.KeyType import KeyType
from csw.Units import Units
from csw.Coords import ProperMotion, EqCoord
from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ParameterSetType import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import Parameter
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


# noinspection PyTypeChecker,PyBroadException
class MyComponentHandlers(ComponentHandlers):
    log = structlog.get_logger()
    prefix = Prefix(Subsystems.CSW, "pycswTest")
    commandServer: CommandServer = None
    dir = pathlib.Path(__file__).parent.absolute()
    outFileName = "PyTestAssemblyCommandResponses.out"
    tmpOutFile = f"/tmp/{outFileName}"
    outFile = f"{dir}/{outFileName}"

    def cleanup(self):
        self.showTestResults()
        if os.path.exists(self.tmpOutFile):
            os.remove(self.tmpOutFile)

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(1)
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        await self.publishCurrentStates()
        await asyncio.sleep(1)
        self.log.debug("Long running task completed")
        return Completed(runId)

    # Checks the command's contents, shows how to access the parameters
    # See ./testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#makeTestCommand
    # for where the command was created.
    # noinspection PyUnresolvedReferences
    def _checkCommand(self, command: ControlCommand):
        try:
            assert (command.get("cmdValue").values == [1.0, 2.0, 3.0])
            assert (list(command.get("cmdValue").values)[0] == 1.0)

            # Access a coordinate value
            eqCoord: EqCoord = list(command.get("BasePosition").values)[0]
            assert (eqCoord.pm == ProperMotion(0.5, 2.33))
            assert (eqCoord.ra == Angle("12:13:14.15 hours"))
            assert (eqCoord.dec == Angle("-30:31:32.3 deg"))

        except:
            self.log.debug(f"_checkCommand: {colored('TEST FAILED', 'red')}")
            traceback.print_exc()

    def showTestResults(self):
        # compare file created by assembly with known good version
        self.log.debug(f"Comparing results: {self.outFile}, {self.tmpOutFile}")
        assert filecmp.cmp(self.outFile, self.tmpOutFile, False)
        self.log.debug(f"{colored('TEST PASSED', 'green')}.")

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component.
        See ./testSupport/test-assembly/src/main/scala/org/tmt/csw/testassembly/TestAssemblyHandlers.scala#makeTestCommand
        for the contents of the command's parameters.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: (CommandResponse, Task)
            a pair: (subclass of CommandResponse, Task), where the task can be None if the command response is final.
            For long running commands, you can respond with Started(runId, "...") and a task that completes the work in the background.
        """
        self._checkCommand(command)
        n = len(command.paramSet)
        self.log.debug(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        # filt = command.get("filter").values[0]
        # encoder = command.get("encoder").values[0]
        # self.log.debug(f"filter = {filt}, encoder = {encoder}")

        if command.commandName.name == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId, "Long running task in progress..."), task
        elif command.commandName.name == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName.name == "ResultCommand":
            result = Result([Parameter("myValue", KeyType.DoubleKey, [42.0])])
            return Completed(runId, result), None
        elif command.commandName.name == "ErrorCommand":
            return Error(runId, "Error command received"), None
        elif command.commandName.name == "InvalidCommand":
            return Invalid(runId, MissingKeyIssue("Missing required key XXX")), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName.name}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
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
    def currentStates(self) -> List[CurrentState]:
        intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
        intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                                    Units.marcsec)
        intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)
        utcTimeParam = Parameter("UTCTimeValue", KeyType.UTCTimeKey, [UTCTime.from_str("2021-09-17T09:17:08.608242344Z")])
        taiTimeParam = Parameter("TAITimeValue", KeyType.TAITimeKey, [TAITime.from_str("2021-09-17T09:17:45.610701219Z")])
        params = [intParam, intArrayParam, floatArrayParam, intMatrixParam, utcTimeParam, taiTimeParam]
        return [CurrentState(self.prefix, "PyCswState", params)]


def test_command_server():
    handlers = MyComponentHandlers()
    commandServer = CommandServer(handlers.prefix, handlers)
    handlers.commandServer = commandServer
    print(f"Starting test command server on port {commandServer.port}")
    try:
        commandServer.start()
    except GracefulExit:
        pass
    handlers.cleanup()
