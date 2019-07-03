from csw.CommandResponse import SubmitResponse, CompletedWithResult, Result
from csw.CommandServer import CommandServer, CommandHandler
from csw.Parameter import Parameter
from csw.Setup import Setup


class MyCommandHandler(CommandHandler):
    def onSubmit(self, setup: Setup) -> SubmitResponse:
        """
        Overrides the base class onSubmit method to handle Submit messages from a CSW component
        :param setup: contains the Submit command from CSW
        :return: a subclass of SubmitResponse that is serialized and passed back to the CSW component
        """
        n = len(setup.paramSet)
        print(f"MyCommandHandler Received setup {str(setup)} with {n} params")
        filt = setup.get("filter").items[0]
        encoder = setup.get("encoder").items[0]
        print(f"filter = {filt}, encoder = {encoder}")

        # --- Example return values ---

        # return Completed(setup.runId)

        # return Error(setup.runId, "There is a problem ...")

        # return Invalid(setup.runId, MissingKeyIssue("Missing required key XXX"))

        return CompletedWithResult(setup.runId, Result("tcs.filter", [Parameter("myValue", 'DoubleKey', [42.0])]))

    def onOneway(self, setup: Setup):
        """
        Overrides the base class onOneway method to handle Submit messages from a CSW component.
        No response os required.
        :param setup: contains the Submit command from CSW
        """
        n = len(setup.paramSet)
        print(f"MyCommandHandler Received oneway {str(setup)} with {n} params")
        filt = setup.get("filter").items[0]
        encoder = setup.get("encoder").items[0]
        print(f"filter = {filt}, encoder = {encoder}")


# noinspection PyTypeChecker
commandServer = CommandServer("pycswTest", MyCommandHandler)
