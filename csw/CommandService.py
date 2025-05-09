import asyncio
import uuid
from asyncio import Task
from datetime import timedelta
from typing import List, Callable, Awaitable

import structlog
from websockets.asyncio.client import connect
from aiohttp import ClientSession

from csw.CommandResponse import SubmitResponse, Error, CommandResponse, Started, ValidateResponse, OnewayResponse
from csw.CommandServiceRequest import Submit, Validate, Oneway, QueryFinal, SubscribeCurrentState, \
    ExecuteDiagnosticMode, ExecuteOperationsMode, GoOnline, GoOffline
from csw.CurrentState import CurrentState
from csw.LocationService import ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.LocationServiceSync import LocationServiceSync
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
import json
from dataclasses import dataclass

from csw.TMTTime import UTCTime
from esw.SequencerRequest import Query


@dataclass
class Subscription:
    task: Task

    def cancel(self):
        self.task.cancel()


# logging.basicConfig(
#     format="%(asctime)s %(message)s",
#     level=logging.DEBUG,
# )


# A CSW command service client
# noinspection PyProtectedMember
class CommandService:

    def __init__(self, prefix: Prefix, componentType: ComponentType, clientSession: ClientSession):
        self.prefix = prefix
        self.componentType = componentType
        self._session = clientSession
        self.log = structlog.get_logger()


    def _getBaseUri(self) -> str:
        locationService = LocationServiceSync()
        connection = ConnectionInfo.make(self.prefix, self.componentType, ConnectionType.HttpType)
        location = locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    async def _postCommand(self, command: str, controlCommand: ControlCommand) -> SubmitResponse:
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
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, await response.text())
        resp = CommandResponse._fromDict(await response.json())
        return resp

    async def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        """
        Submits a command to the command service

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        return await self._postCommand("Submit", controlCommand)

    async def validate(self, controlCommand: ControlCommand) -> ValidateResponse:
        """
        Validates a command to be sent to the command service.

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse (only Accepted, Invalid or Locked)
       """
        return await self._postCommand("Validate", controlCommand)

    async def oneway(self, controlCommand: ControlCommand) -> OnewayResponse:
        """
       Sends a command to the command service without expecting a reply.

       Args:
           controlCommand (ControlCommand): command to submit

       Returns: SubmitResponse
           a subclass of SubmitResponse (only Accepted, Invalid or Locked)
      """
        return await self._postCommand("Oneway", controlCommand)

    # noinspection DuplicatedCode
    async def queryFinal(self, runId: str, timeout: timedelta) -> SubmitResponse:
        """
        If the command for runId returned Started (long-running command), this will
        return the final result.

       Args:
           runId (str): runId for the command
           timeout (timedelta): timr to wait before returning an error

       Returns: SubmitResponse
           a subclass of SubmitResponse
      """
        baseUri = (self._getBaseUri()).replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = QueryFinal(runId, timeout)._asDict()
        jsonStr = json.dumps(msgDict)
        ws = await self._session.ws_connect(wsUri)
        await ws.send_str(jsonStr)
        jsonResp = await ws.receive_str()
        await ws.close()
        return CommandResponse._fromDict(json.loads(jsonResp))

    async def submitAndWaitAsync(self, controlCommand: ControlCommand, timeout: timedelta) -> SubmitResponse:
        """
        Submits a command to the command service and waits for the final response.
        This version returns a future response (async).
        See submitAndWait() for a blocking version.

        Args:
            controlCommand (ControlCommand): command to submit
            timeout (timedelta): time to wait before returning an error

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        resp = await self.submit(controlCommand)
        match resp:
            case Started(runId):
                return await self.queryFinal(runId, timeout)
            case _:
                return resp

    # noinspection DuplicatedCode
    async def query(self, runId: str) -> SubmitResponse:
        """
        Query for the result of a long-running command which was sent as Submit to get a SubmitResponse.
        Query allows checking to see if a long-running command is completed without waiting as with queryFinal.

        Args:
           runId (str): runId for the command

        Returns: SubmitResponse
           a subclass of SubmitResponse
        """
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = Query(runId)._asDict()
        jsonData = json.loads(json.dumps(data))
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: query failed: {await response.json()}")
        # return CommandResponse._fromDict(json.loads(await response.json()))
        return CommandResponse._fromDict(await response.json())


    async def submitAndWait(self, controlCommand: ControlCommand, timeout: timedelta) -> SubmitResponse:
        """
        Submits a command to the command service and waits for the final response.

        Args:
            controlCommand (ControlCommand): command to submit
            timeout (timedelta): time to wait before returning an error

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        resp = await self.submit(controlCommand)
        match resp:
            case Started(runId):
                return await self.queryFinal(runId, timeout)
            case _:
                return resp

    async def _subscribeCurrentState(self, names: List[str], callback: Callable[[CurrentState], Awaitable]):
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        msgDict = SubscribeCurrentState(names)._asDict()
        jsonStr = json.dumps(msgDict)
        async with connect(wsUri) as websocket:
            await websocket.send(jsonStr)
            async for message in websocket:
                await callback(CurrentState._fromDict(json.loads(message)))

    # async def _subscribeCurrentState(self, names: List[str], callback: Callable[[CurrentState], Awaitable]):
    #     baseUri = (self._getBaseUri()).replace('http:', 'ws:')
    #     wsUri = f"{baseUri}websocket-endpoint"
    #     msgDict = SubscribeCurrentState(names)._asDict()
    #     jsonStr = json.dumps(msgDict)
    #     print(f"XXX _subscribeCurrentState: json = {jsonStr}")
    #     async with self._session.ws_connect(wsUri) as ws:
    #         await ws.send_str(jsonStr)
    #         async for msgF in ws:
    #             msg = await msgF
    #             print(f"XXX _subscribeCurrentState: message = {msg}")
    #             match msg.type:
    #                 case aiohttp.WSMsgType.TEXT:
    #                     print(f"XXX _subscribeCurrentState: callback({CurrentState._fromDict(json.loads(msg.data))})")
    #                     await callback(CurrentState._fromDict(json.loads(msg.data)))
    #                 case aiohttp.WSMsgType.CLOSED:
    #                     break
    #                 case aiohttp.WSMsgType.ERROR:
    #                     break

    async def subscribeCurrentState(self, names: List[str], callback: Callable[[CurrentState], Awaitable]) -> Subscription:
        """
        Subscribe to the current state of a component

        Args:
           names (List[str]): subscribe to states which have any of the provided value for name.
                              If no states are provided, all the current states will be received.
           callback: a function to be called with the CurrentState values

        Returns: subscription task
        """
        task = asyncio.create_task(self._subscribeCurrentState(names, callback))
        await asyncio.sleep(0.1) # XXX TODO FIXME: Need to wait for task to startup
        return Subscription(task)

    async def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
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
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: executeDiagnosticMode failed: {await response.text()}")

    async def executeOperationsMode(self):
        """
        On receiving a operations mode command, the current diagnostic data mode is halted.
        """
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = ExecuteOperationsMode()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: executeOperationsMode failed: {await response.text()}")

    async def goOnline(self):
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = GoOnline()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: goOnline failed: {await response.text()}")

    async def goOffline(self):
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        data = GoOffline()._asDict()
        jsonData = json.loads(json.dumps(data))
        response = await self._session.post(postUri, headers=headers, json=jsonData)
        if not response.ok:
            raise Exception(f"CommandService: goOffline failed: {await response.text()}")
