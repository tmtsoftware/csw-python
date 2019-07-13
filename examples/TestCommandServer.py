from csw.CommandResponse import CommandResponse, CompletedWithResult, Result, Completed, Invalid, MissingKeyIssue, \
    Error, Accepted
from csw.CommandServer import CommandServer, CommandHandler
from csw.ControlCommand import ControlCommand
from csw.Parameter import Parameter


class MyCommandHandler(CommandHandler):
    def onSubmit(self, command: ControlCommand) -> CommandResponse:
        """
        Overrides the base class onSubmit method to handle commands from a CSW component
        :param command: contains the ControlCommand from CSW
        :return: a subclass of CommandResponse that is serialized and passed back to the CSW component
        """
        n = len(command.paramSet)
        print(f"MyCommandHandler Received setup {str(command)} with {n} params")
        # filt = command.get("filter").items[0]
        # encoder = command.get("encoder").items[0]
        # print(f"filter = {filt}, encoder = {encoder}")

        # --- Example return values ---

        # return Completed(command.runId)

        # return Error(command.runId, "There is a problem ...")

        # return Invalid(command.runId, MissingKeyIssue("Missing required key XXX"))

        return CompletedWithResult(command.runId, Result("tcs.filter", [Parameter("myValue", 'DoubleKey', [42.0])]))

    def onOneway(self, command: ControlCommand):
        """
        Overrides the base class onOneway method to handle commands from a CSW component.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        n = len(command.paramSet)
        print(f"MyCommandHandler Received oneway {str(command)} with {n} params")
        filt = command.get("filter").items[0]
        encoder = command.get("encoder").items[0]
        print(f"filter = {filt}, encoder = {encoder}")
        return Accepted(command.runId)

    def validate(self, command: ControlCommand):
        """
        Overrides the base class validate method to verify that the given command is valid.
        :param command: contains the ControlCommand from CSW
        :return: an instance of one of these command responses: Accepted, Invalid, Locked (OnewayResponse in CSW)
        """
        return Accepted(command.runId)

# noinspection PyTypeChecker
commandServer = CommandServer("pycswTest", MyCommandHandler)
