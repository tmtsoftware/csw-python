import json
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


@dataclass
@dataclass_json
class Validate:
    controlCommand: ControlCommand


@dataclass
@dataclass_json
class Submit:
    controlCommand: ControlCommand


@dataclass
@dataclass_json
class Oneway:
    controlCommand: ControlCommand


@dataclass
@dataclass_json
class QueryFinal:
    runId: str
    timeout: str

    @staticmethod
    def fromDict(obj):
        """
        Returns a ControlCommand for the given dict.
        """
        typ = next(iter(obj))
        obj = obj[typ]
        runId = obj['runId']
        timeout = obj['timeout']
        return QueryFinal(runId, timeout)

@dataclass
@dataclass_json
class SubscribeCurrentState:
    stateNames: List[str]

    @staticmethod
    def fromDict(obj):
        """
        Returns a SubscribeCurrentState for the given dict.
        """
        typ = next(iter(obj))
        stateNames = obj[typ]
        return SubscribeCurrentState(stateNames)

class CommandServer:
    """
    Creates an HTTP server that can receive CSW commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.
    """
    crm = CommandResponseManager()

    async def _handlePost(self, request: Request) -> Response:
        obj = await request.json()
        method = next(iter(obj))
        if method in {'Submit', 'Oneway', 'Validate'}:
            command = ControlCommand.fromDict(obj[method])
            runId = str(uuid.uuid4())
            if method == 'Submit':
                commandResponse, task = self.handler.onSubmit(runId, command)
                if task is not None:
                    # noinspection PyTypeChecker
                    self.crm.addTask(runId, task)
                    print("A task is still running")
            elif method == 'Oneway':
                commandResponse = self.handler.onOneway(runId, command)
            else:
                commandResponse = self.handler.validateCommand(runId, command)
            responseDict = commandResponse.asDict()
            return web.json_response(responseDict)
        else:
            raise Exception("Invalid Location type: " + method)

    async def _handleQueryFinal(self, queryFinal: QueryFinal) -> Response:
        commandResponse = await self.crm.waitForTask(queryFinal.runId)  # XXX TODO: timeout
        responseDict = commandResponse.asDict()
        return web.json_response(responseDict)

    async def _handleWs(self, request: Request) -> WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        msg: WSMessage
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    obj = json.loads(msg.data)
                    method = next(iter(obj))
                    # '{"QueryFinal":{"runId":"396195e9-34d6-468c-bcfd-6def4b5e74a0","timeout":[20,"SECONDS"]}}'
                    if method == "QueryFinal":
                        queryFinal = QueryFinal.fromDict(obj)
                        resp = await self._handleQueryFinal(queryFinal)
                        await ws.send_str(resp.text)
                        await ws.close()
                    elif method == "SubscribeCurrentState":
                        stateNames = SubscribeCurrentState.fromDict(obj).stateNames
                        print(f"Received SubscribeCurrentState: stateNames = {stateNames}")
                        self.handler._subscribeCurrentState(stateNames, ws)
                    else:
                        print(f"Warning: Received unknown ws message: {str(msg.data)}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('Error: ws connection closed with exception %s' % ws.exception())
        print('websocket connection closed')
        return ws

    @staticmethod
    def _registerWithLocationService(prefix: str, port: int):
        print("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo(prefix, ComponentType.Service.value, ConnectionType.HttpType.value)
        atexit.register(locationService.unregister, connection)
        locationService.register(HttpRegistration(connection, port, "/post-endpoint"))

    def __init__(self, prefix: str, handler: ComponentHandlers, port: int = 8082, currentStatePublishSeconds: int = 2):
        self.handler = handler
        app = web.Application()
        app.add_routes([
            web.post('/post-endpoint', self._handlePost),
            web.get("/websocket-endpoint", self._handleWs)
        ])
        self._registerWithLocationService(prefix, port)
        web.run_app(app, port=port)