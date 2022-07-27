import asyncio
from asyncio import Task
from typing import List

from csw.CommandResponse import CommandResponse, Result, Completed, Invalid, \
    Accepted, Started, UnsupportedCommandIssue
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ParameterSetType import ControlCommand
from csw.CurrentState import CurrentState
from csw.Parameter import IntKey, UTCTimeKey, TAITimeKey, IntArrayKey, FloatArrayKey, IntMatrixKey, DoubleKey
from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


class MyComponentHandlers(ComponentHandlers):
    prefix = Prefix(Subsystems.CSW, "pycswTest")

    async def longRunningCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(3)
        print("Long running task completed")
        # TODO: Do this in a timer task
        await self.publishCurrentStates()
        return Completed(runId)

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW

        Returns: (CommandResponse, Task)
            a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")

        if command.commandName.name == "LongRunningCommand":
            task = asyncio.create_task(self.longRunningCommand(runId, command))
            return Started(runId), task
        elif command.commandName.name == "SimpleCommand":
            return Completed(runId), None
        elif command.commandName.name == "ResultCommand":
            param = DoubleKey.make("myValue").set(42.0)
            result = Result([param])
            return Completed(runId, result), None
        else:
            return Invalid(runId, UnsupportedCommandIssue(f"Unknown command: {command.commandName.name}")), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onOneway method to handle commands from a CSW component.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW

        Returns: CommandResponse
            an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params")
        return Accepted(runId)

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the ControlCommand from CSW

        Returns: CommandResponse
            an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(runId)

    # Returns the current state
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


# noinspection PyTypeChecker
handlers = MyComponentHandlers()
commandServer = CommandServer(handlers.prefix, handlers)
print(f"Starting test command server on port {commandServer.port}")
commandServer.start()
