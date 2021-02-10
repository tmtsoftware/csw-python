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

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: (CommandResponse, Task)
            a pair: (subclass of CommandResponse, Task), where the task can be None if the command response is final.
            For long running commands, you can respond with Started(runId, "...") and a task that completes the work in the background.
        """
        # noinspection PyTypeChecker
        return Error(runId, "Not implemented: submit command handler"), None

    def onOneway(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Handles the given setup command and returns an immediate CommandResponse

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        return Error(runId, "Not implemented: oneway command handler")

    def validateCommand(self, runId: str, command: ControlCommand) -> CommandResponse:
        """
        Validates the given command

        Args:
            runId (str): unique id for this command
            command (ControlCommand): contains the command

        Returns: CommandResponse
            a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
       """
        return Accepted(runId)

    def currentStates(self) -> List[CurrentState]:
        """
        Returns the current states for the component
        """
        return []

    # ---Do not override the following methods ---

    async def publishCurrentStates(self):
        """
        Publish the current state of the python based CSW component
        """
        for currentState in self.currentStates():
            s1 = self._currentStateSubscribers.get("") or set()
            s2 = self._currentStateSubscribers.get(currentState.stateName) or set()
            subscribers = s1 | s2
            dict = currentState._asDict()
            cs = json.dumps(dict)
            for ws in subscribers:
                print(f"Publishing current state: {cs}")
                await ws.send_str(cs)

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

    def _unsubscribeCurrentState(self, ws: WebSocketResponse):
        """
        Internal method used to unsubscribe a websocket from current state events
        """
        for stateName in self._currentStateSubscribers:
            if ws in self._currentStateSubscribers[stateName]:
                self._currentStateSubscribers[stateName].remove(ws)
