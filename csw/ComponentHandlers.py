from csw.CommandResponse import CommandResponse, Accepted, Error
from csw.ControlCommand import ControlCommand
from asyncio import Task


class ComponentHandlers:
    """
    Abstract base class for handling CSW commands.
    Subclasses can override methods to implement the behavior of the component.
    """

    def onSubmit(self, runId: str, command: ControlCommand) -> (CommandResponse, Task):
        """
        Handles the given setup command and returns a CommandResponse subclass
        :param runId: unique id for this command
        :param command: contains the command
        :return: a pair: (subclass of CommandResponse, Task),
        where the task can be None if the command response is final.
        For long running commands, you can respond with Started(runId, "...") and a task that
        completes the work in the background.
        """
        return Error(runId, "Not implemented: submit command handler"), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Handles the given setup command and returns an immediate CommandResponse
        :param runId: unique id for this command
        :param command: contains the command
        :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        return Error(runId, "Not implemented: oneway command handler")

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
       Validates the given command
        :param runId: unique id for this command
       :param command: contains the command
       :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
       """
        return Accepted(runId)
