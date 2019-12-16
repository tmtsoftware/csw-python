import json
from typing import List

from aiohttp.web_ws import WebSocketResponse

from csw.CommandResponse import CommandResponse, Accepted, Error
from csw.ControlCommand import ControlCommand
from asyncio import Task

from csw.CurrentState import CurrentState


class ComponentHandlers:
    """
    Abstract base class for handling CSW commands.
    Subclasses can override onSubmit, onOneway, validateCommand, and currentState to implement the behavior of the
    component.
    """

    # map of current state name to list of websockets going to subscribers
    _currentStateSubscribers = {}

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

    def currentStates(self) -> List[CurrentState]:
        """
        Returns the current state for the component
        :stateName str: the name of the current state to get
        """
        return []

    # ---Do not override the following methods ---

    def publishCurrentState(self, currentState: CurrentState):
        """
        Publish the current state of the python based CSW component
        """
        subscribers = self._currentStateSubscribers[""] | self._currentStateSubscribers[currentState.stateName]
        cs = json.dumps(currentState.asDict())
        for ws in subscribers:
            ws.send_str(cs)

    def _addCurrentStateSubscriber(self, stateName: str, ws: WebSocketResponse):
        if (stateName in self._currentStateSubscribers):
            self._currentStateSubscribers[stateName].add(ws)
        else:
            self._currentStateSubscribers[stateName] = {ws}

    def _subscribeCurrentState(self, stateNames: List[str], ws: WebSocketResponse):
        """
        Internal method used to subscribe to current state of this component.
        If stateNames is empty, subscribe to all current states
        """
        if len(stateNames) == 0:
            self._addCurrentStateSubscriber("", ws)
        else:
            for stateName in stateNames:
                self._addCurrentStateSubscriber(stateName, ws)
