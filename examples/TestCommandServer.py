from csw.CommandResponse import SubmitResponse, CompletedWithResult, Result, Completed, Invalid, MissingKeyIssue, Error
from csw.CommandServer import CommandServer, CommandHandler
from csw.ControlCommand import ControlCommand
from csw.Parameter import Parameter


class MyCommandHandler(CommandHandler):
    def onSubmit(self, command: ControlCommand) -> SubmitResponse:
        """
        Overrides the base class onSubmit method to handle Submit messages from a CSW component
        :param command: contains the ControlCommand from CSW
        :return: a subclass of SubmitResponse that is serialized and passed back to the CSW component
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
        Overrides the base class onOneway method to handle Submit messages from a CSW component.
        No response os required.
        :param command: contains the ControlCommand from CSW
        """
        n = len(command.paramSet)
        print(f"MyCommandHandler Received oneway {str(command)} with {n} params")
        filt = command.get("filter").items[0]
        encoder = command.get("encoder").items[0]
        print(f"filter = {filt}, encoder = {encoder}")


# noinspection PyTypeChecker
commandServer = CommandServer("pycswTest", MyCommandHandler)
