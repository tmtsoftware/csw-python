import asyncio
import uuid
from asyncio import Task
from http.client import responses
from typing import List, Callable

import requests
import websockets
from websocket import create_connection

from csw.CommandResponse import SubmitResponse, Error, CommandResponse, Started, ValidateResponse, OnewayResponse
from csw.CommandServiceRequest import Submit, Validate, Oneway, QueryFinal, SubscribeCurrentState, \
    ExecuteDiagnosticMode, ExecuteOperationsMode, GoOnline, GoOffline
from csw.CurrentState import CurrentState
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
import json
from dataclasses import dataclass

from csw.UTCTime import UTCTime
from esw.SequencerRequest import Query


@dataclass
class Subscription:
    task: Task

    def cancel(self):
        self.task.cancel()


# A CSW command service client
# noinspection PyProtectedMember
@dataclass
class CommandService:
    prefix: Prefix
    componentType: ComponentType

    def _getBaseUri(self) -> str:
        locationService = LocationService()
        connection = ConnectionInfo.make(self.prefix, self.componentType, ConnectionType.HttpType)
        location = locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    def _postCommand(self, command: str, controlCommand: ControlCommand) -> SubmitResponse:
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        match command:
            case 'Submit':
                data = Submit(controlCommand)._asDict()
            case 'Validate':
                data = Validate(controlCommand)._asDict()
            case _:
                data = Oneway(controlCommand)._asDict()
        jsonData = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, response.text)
        resp = CommandResponse._fromDict(response.json())
        return resp

    # def _wsCommand(self, command: str, controlCommand: ControlCommand) -> SubmitResponse:
    #     baseUri = self._getBaseUri().replace('http:', 'ws:')
    #     wsUri = f"{baseUri}websocket-endpoint"

    def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        """
        Submits a command to the command service

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        return self._postCommand("Submit", controlCommand)

    def validate(self, controlCommand: ControlCommand) -> ValidateResponse:
        """
        Validates a command to be sent to the command service.

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse (only Accepted, Invalid or Locked)
       """
        return self._postCommand("Validate", controlCommand)

    def oneway(self, controlCommand: ControlCommand) -> OnewayResponse:
        """
       Sends a command to the command service without expecting a reply.

       Args:
           controlCommand (ControlCommand): command to submit

       Returns: SubmitResponse
           a subclass of SubmitResponse (only Accepted, Invalid or Locked)
      """
        return self._postCommand("Oneway", controlCommand)

    async def queryFinalAsync(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        """
        If the command for runId returned Started (long running command), this will
        return the final result.
        This version returns a future response (async).
        See queryFinal() for a blocking version.

       Args:
           runId (str): runId for the command
           timeoutInSeconds (int): seconds to wait before returning an error

       Returns: SubmitResponse
           a subclass of SubmitResponse
      """
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = QueryFinal(runId, timeoutInSeconds)._asDict()
        jsonStr = json.dumps(msgDict)
        async with websockets.connect(wsUri) as websocket:
            await websocket.send(jsonStr)
            jsonResp = await websocket.recv()
            return CommandResponse._fromDict(json.loads(jsonResp))

    async def submitAndWaitAsync(self, controlCommand: ControlCommand, timeoutInSeconds: int) -> SubmitResponse:
        """
        Submits a command to the command service and waits for the final response.
        This version returns a future response (async).
        See submitAndWait() for a blocking version.

        Args:
            controlCommand (ControlCommand): command to submit
            timeoutInSeconds (int): seconds to wait before returning an error

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        resp = self.submit(controlCommand)
        match resp:
            case Started(runId):
                return await self.queryFinalAsync(runId, timeoutInSeconds)
            case _:
                return resp

    def query(self, runId: str) -> SubmitResponse:
        """
        Query for the result of a long running command which was sent as Submit to get a SubmitResponse.
        Query allows checking to see if a long-running command is completed without waiting as with queryFinal.

        Args:
           runId (str): runId for the command

        Returns: SubmitResponse
           a subclass of SubmitResponse
        """
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = Query(runId)._asDict()
        jsonStr = json.dumps(msgDict)
        ws = create_connection(wsUri)
        ws.send(jsonStr)
        jsonResp = ws.recv()
        return CommandResponse._fromDict(json.loads(jsonResp))

    def queryFinal(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        """
        If the command for runId returned Started (long-running command), this will
        return the final result.

       Args:
           runId (str): runId for the command
           timeoutInSeconds (int): seconds to wait before returning an error

       Returns: SubmitResponse
           a subclass of SubmitResponse
      """
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = QueryFinal(runId, timeoutInSeconds)._asDict()
        jsonStr = json.dumps(msgDict)
        ws = create_connection(wsUri)
        ws.send(jsonStr)
        jsonResp = ws.recv()
        return CommandResponse._fromDict(json.loads(jsonResp))

    def submitAndWait(self, controlCommand: ControlCommand, timeoutInSeconds: int) -> SubmitResponse:
        """
        Submits a command to the command service and waits for the final response.

        Args:
            controlCommand (ControlCommand): command to submit
            timeoutInSeconds (int): seconds to wait before returning an error

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        resp = self.submit(controlCommand)
        match resp:
            case Started(runId):
                return self.queryFinal(runId, timeoutInSeconds)
            case _:
                return resp

    async def _subscribeCurrentState(self, names: List[str], callback: Callable[[CurrentState], None]):
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = SubscribeCurrentState(names)._asDict()
        jsonStr = json.dumps(msgDict)
        async for websocket in websockets.connect(wsUri):
            await websocket.send(jsonStr)
            async for message in websocket:
                callback(CurrentState._fromDict(json.loads(message)))

    def subscribeCurrentState(self, names: List[str], callback: Callable[[CurrentState], None]) -> Subscription:
        """
        Subscribe to the current state of a component

        Args:
           names (List[str]): subscribe to states which have any of the provided value for name.
                              If no states are provided, all the current states will be received.
           callback: a function to be called with the CurrentState values

        Returns: subscription task
        """
        task = asyncio.create_task(self._subscribeCurrentState(names, callback))
        return Subscription(task)

    def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        On receiving a diagnostic data command, the component goes into a diagnostic data mode based on hint at the specified startTime.
        Validation of supported hints need to be handled by the component writer.

        Args:
            startTime: represents the time at which the diagnostic mode actions will take effect
            hint: represents supported diagnostic data mode for a component
        """
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = ExecuteDiagnosticMode(startTime, hint)._asDict()
        jsonData = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: executeDiagnosticMode failed: {response.text}")

    def executeOperationsMode(self):
        """
        On receiving a operations mode command, the current diagnostic data mode is halted.
        """
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = ExecuteOperationsMode()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: executeOperationsMode failed: {response.text}")

    def goOnline(self):
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = GoOnline()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: goOnline failed: {response.text}")

    def goOffline(self):
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = GoOffline()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: goOffline failed: {response.text}")
