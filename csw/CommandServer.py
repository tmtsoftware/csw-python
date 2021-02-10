import json
import traceback
from dataclasses import dataclass
from typing import List

import aiohttp
from aiohttp import web, WSMessage
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit
import uuid

from aiohttp.web_ws import WebSocketResponse
from dataclasses_json import dataclass_json

from csw.CommandResponseManager import CommandResponseManager
from csw.ComponentHandlers import ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration

# Ignore generated functions in API docs
__pdoc__ = {}


def _pdocIgnoreGenerated(className: str):
    __pdoc__[f"{className}.from_dict"] = False
    __pdoc__[f"{className}.from_json"] = False
    __pdoc__[f"{className}.schema"] = False
    __pdoc__[f"{className}.to_dict"] = False
    __pdoc__[f"{className}.to_json"] = False


_pdocIgnoreGenerated("Validate")


@dataclass_json
@dataclass
class Validate:
    """
    A message sent to validate a command. The response should be one of: Accepted, Invalid or Locked.

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("Submit")


@dataclass_json
@dataclass
class Submit:
    """
    Represents a command that requires a response (of type CommandResponse).

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("Oneway")


@dataclass_json
@dataclass
class Oneway:
    """
    Represents a command that does not require or expect a response

    Args:
        controlCommand (ControlCommand): The command to send
    """
    controlCommand: ControlCommand


_pdocIgnoreGenerated("QueryFinal")


@dataclass_json
@dataclass
class QueryFinal:
    """
    A message sent to query the final result of a long running command.
    The response should be a CommandResponse.

    Args:
        runId (str): The command's runId
        timeoutInSeconds (int) amount of time to wait
    """
    runId: str
    timeoutInSeconds: int

    @staticmethod
    def _fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        try:
            runId = obj['runId']
            timeoutInSeconds = obj['timeoutInSeconds']
            return QueryFinal(runId, timeoutInSeconds)
        except:
            traceback.print_exc()


_pdocIgnoreGenerated("SubscribeCurrentState")


@dataclass_json
@dataclass
class SubscribeCurrentState:
    """
    Message used to subscribe to the current state of a component.

    Args:
        stateNames (List[str]) list of current state names to subscribe to
    """
    stateNames: List[str]

    @staticmethod
    def _fromDict(obj):
        """
        Returns a SubscribeCurrentState for the given dict.
        """
        # typ = obj["_type"]
        if "names" in obj.keys():
            stateNames = obj.get("names")
        else:
            stateNames = []
        return SubscribeCurrentState(stateNames)


class CommandServer:
    _app = web.Application()
    _crm = CommandResponseManager()

    async def _handlePost(self, request: Request) -> Response:
        obj = await request.json()
        # print(f"received post: {str(obj)}")
        method = obj['_type']
        if method in {'Submit', 'Oneway', 'Validate'}:
            command = ControlCommand._fromDict(obj['controlCommand'])
            runId = str(uuid.uuid4())
            if method == 'Submit':
                commandResponse, task = self.handler.onSubmit(runId, command)
                if task is not None:
                    # noinspection PyTypeChecker
                    self._crm.addTask(runId, task)
                    print("Long running task in progress...")
            elif method == 'Oneway':
                commandResponse = self.handler.onOneway(runId, command)
            else:
                commandResponse = self.handler.validateCommand(runId, command)
            responseDict = commandResponse._asDict()
            return web.json_response(responseDict)
        else:
            raise Exception("Invalid command type: " + method)

    async def _handleQueryFinal(self, queryFinal: QueryFinal) -> Response:
        commandResponse = await self._crm.waitForTask(queryFinal.runId, queryFinal.timeoutInSeconds)
        responseDict = commandResponse._asDict()
        return web.json_response(responseDict)

    async def _handleWs(self, request: Request) -> WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        msg: WSMessage
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    print("Received ws close message")
                    await ws.close()
                else:
                    obj = json.loads(msg.data)
                    # print(f"received message: {str(obj)}")
                    method = obj['_type']
                    if method == "QueryFinal":
                        queryFinal = QueryFinal._fromDict(obj)
                        resp = await self._handleQueryFinal(queryFinal)
                        await ws.send_str(resp.text)
                        await ws.close()
                    elif method == "SubscribeCurrentState":
                        stateNames = SubscribeCurrentState._fromDict(obj).stateNames
                        print(f"Received SubscribeCurrentState: stateNames = {stateNames}")
                        self.handler._subscribeCurrentState(stateNames, ws)
                    else:
                        print(f"Warning: Received unknown ws message: {str(msg.data)}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('Error: ws connection closed with exception %s' % ws.exception())
        print('websocket connection closed')
        self.handler._unsubscribeCurrentState(ws)
        return ws

    @staticmethod
    def _registerWithLocationService(prefix: str, port: int):
        print("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo(prefix, ComponentType.Service.value, ConnectionType.HttpType.value)
        atexit.register(locationService.unregister, connection)
        # locationService.unregister(connection)
        locationService.register(HttpRegistration(connection, port, "/post-endpoint"))

    def __init__(self, prefix: str, handler: ComponentHandlers, port: int = 8082):
        """
        Creates an HTTP server that can receive CSW commands and registers it with the Location Service using the given prefix,
        so that CSW components can locate it and send commands to it.

        Args:
            prefix (str): a CSW Prefix in the format $subsystem.name, where subsystem is one of the upper case TMT
                          subsystem names and name is the name of the command server
            handler (ComponentHandlers): command handler notified when commands are received
            port (int): optional port for HTTP server
        """
        self.handler = handler
        self.port = port
        self._app.add_routes([
            web.post('/post-endpoint', self._handlePost),
            web.get("/websocket-endpoint", self._handleWs)
        ])
        self._registerWithLocationService(prefix, port)

    def start(self):
        """
        Starts the command http server in a thread
        """
        web.run_app(self._app, port=self.port)
