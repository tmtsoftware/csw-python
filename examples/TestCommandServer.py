import asyncio
from asyncio import Task

from csw.CommandResponse import CommandResponse, CompletedWithResult, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted, Started
from csw.CommandServer import CommandServer, ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.Parameter import Parameter


class MyComponentHandlers(ComponentHandlers):

    async def longRunningCommand(self, command: ControlCommand) -> CommandResponse:
        await asyncio.sleep(5)
        print("XXX Long running task completed")
        return Completed(command.runId)

    def onSubmit(self, command: ControlCommand) -> (CommandResponse, Task):
        """
        Overrides the base class onSubmit method to handle commands from a CSW component
        :param command: contains the ControlCommand from CSW
        :return: a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received setup {str(command)} with {n} params")
        # filt = command.get("filter").items[0]
        # encoder = command.get("encoder").items[0]
        # print(f"filter = {filt}, encoder = {encoder}")

        # --- Example return values ---

        # return Completed(command.runId), None

        # return Error(command.runId, "There is a problem ..."), None

        # return Invalid(command.runId, MissingKeyIssue("Missing required key XXX")), None

        # result = Result("tcs.filter", [Parameter("myValue", 'DoubleKey', [42.0])])
        # return CompletedWithResult(command.runId, result), None

        # long running command
        task = asyncio.create_task(self.longRunningCommand(command))
        return Started(command.runId, "Long running task in progress..."), task

    def onOneway(self, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onOneway method to handle commands from a CSW component.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyComponentHandlers Received oneway {str(command)} with {n} params")
        filt = command.get("filter").items[0]
        encoder = command.get("encoder").items[0]
        print(f"filter = {filt}, encoder = {encoder}")
        return Accepted(command.runId)

    def validateCommand(self, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class validate method to verify that the given command is valid.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(command.runId)


# noinspection PyTypeChecker
commandServer = CommandServer("pycswTest", MyComponentHandlers())
