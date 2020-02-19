import signal
import sys
import os
import asyncio
from asyncio import Task
from datetime import datetime
from threading import Timer
from typing import List

from aiohttp.web_runner import GracefulExit

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import Parameter

class MyComponentHandlers(ComponentHandlers):
    prefix = "CSW.pycswTest"
    commandServer: CommandServer = None

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(3)
        print("Long running task completed")
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        return Completed(runId)

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component
        :param runId: unique id for this command
        :param command: contains the ControlCommand from CSW
        :return: a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        # filt = command.get("filter").values[0]
        # encoder = command.get("encoder").values[0]
        # print(f"filter = {filt}, encoder = {encoder}")

        if command.commandName == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId, "Long running task in progress..."), task
        elif command.commandName == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName == "ResultCommand":
            result = Result([Parameter("myValue", 'DoubleKey', [42.0])])
            return Completed(runId, result), None
        elif command.commandName == "ErrorCommand":
            return Error(runId, "Error command received"), None
        elif command.commandName == "InvalidCommand":
            return Invalid(runId, MissingKeyIssue("Missing required key XXX")), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onOneway method to handle commands from a CSW component.
        :param runId: unique id for this command
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params.\nTEST PASSED.")
        raise GracefulExit()

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.
        :param runId: unique id for this command
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(runId)

    # Returns the current state
    def currentStates(self) -> List[CurrentState]:
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")
        return [CurrentState(self.prefix, "PyCswState", [intParam, intArrayParam, floatArrayParam, intMatrixParam])]

def test_command_server():
    handlers = MyComponentHandlers()
    commandServer = CommandServer(handlers.prefix, handlers)
    handlers.commandServer = commandServer
    print(f"Starting test command server on port {commandServer.port}")
    commandServer.start()
