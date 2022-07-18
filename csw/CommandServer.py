import json

import aiohttp
import structlog
from aiohttp import web, WSMessage
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit
import uuid

from aiohttp.web_ws import WebSocketResponse

from csw.CommandResponse import Error
from csw.CommandResponseManager import CommandResponseManager
from csw.CommandServiceRequest import QueryFinal, SubscribeCurrentState
from csw.ComponentHandlers import ComponentHandlers
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration


# noinspection PyProtectedMember
class CommandServer:
    _app = web.Application()
    _crm = CommandResponseManager()
    log = structlog.get_logger()

    async def _handlePost(self, request: Request) -> Response:
        obj = await request.json()
        method = obj['_type']
        runId = str(uuid.uuid4())
        try:
            command: ControlCommand = ControlCommand._fromDict(obj['controlCommand'])
        except TypeError:
            commandResponse = Error(runId, "Invalid command")
            return web.json_response(commandResponse._asDict())

        self.log.info(f"Received command {command}")
        match method:
            case 'Submit':
                commandResponse, task = self.handler.onSubmit(runId, command)
                if task is not None:
                    # noinspection PyTypeChecker
                    self._crm.addTask(runId, task)
                    self.log.debug("Long running task in progress...")
            case 'Oneway':
                commandResponse = self.handler.onOneway(runId, command)
            case 'Validate':
                commandResponse = self.handler.validateCommand(runId, command)
            case x:  # should not happe
                commandResponse = Error(runId, "Invalid command")
        return web.json_response(commandResponse._asDict())

    async def _handleQueryFinal(self, queryFinal: QueryFinal) -> Response:
        commandResponse = await self._crm.waitForTask(queryFinal.runId, queryFinal.timeoutInSeconds)
        responseDict = commandResponse._asDict()
        return web.json_response(responseDict)

    async def _handleWsTextMessage(self, ws: WebSocketResponse, msg: WSMessage):
        if msg.data == 'close':
            self.log.debug("Received ws close message")
            await ws.close()
        else:
            obj = json.loads(msg.data)
            match obj['_type']:
                case "QueryFinal":
                    queryFinal = QueryFinal._fromDict(obj)
                    resp = await self._handleQueryFinal(queryFinal)
                    await ws.send_str(resp.text)
                    await ws.close()
                case "SubscribeCurrentState":
                    stateNames = SubscribeCurrentState._fromDict(obj).stateNames
                    self.log.debug(f"Received SubscribeCurrentState: stateNames = {stateNames}")
                    self.handler._subscribeCurrentState(stateNames, ws)
                case _:
                    self.log.debug(f"Warning: Received unknown ws message: {str(msg.data)}")

    async def _handleWs(self, request: Request) -> WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        msg: WSMessage
        async for msg in ws:
            match msg.type:
                case aiohttp.WSMsgType.TEXT:
                    await self._handleWsTextMessage(ws, msg)
                case aiohttp.WSMsgType.ERROR:
                    self.log.debug('Error: ws connection closed with exception %s' % ws.exception())
        self.log.debug('websocket connection closed')
        self.handler._unsubscribeCurrentState(ws)
        return ws

    def _registerWithLocationService(self, prefix: Prefix, port: int):
        locationService = LocationService()
        connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
        atexit.register(locationService.unregister, connection)
        locationService.register(HttpRegistration(connection, port))

    def __init__(self, prefix: Prefix, handler: ComponentHandlers, port: int = 0):
        """
        Creates an HTTP server that can receive CSW commands and registers it with the Location Service using the given
        prefix, so that CSW components can locate it and send commands to it.

        Args:
            prefix (str): a CSW Prefix in the format $subsystem.name, where subsystem is one of the upper case TMT
                          subsystem names and name is the name of the command server
            handler (ComponentHandlers): command handler notified when commands are received
            port (int): optional port for HTTP server
        """
        self.handler = handler
        self.port = LocationService.getFreePort(port)
        self._app.add_routes([
            web.post('/post-endpoint', self._handlePost),
            web.get("/websocket-endpoint", self._handleWs)
        ])
        self._registerWithLocationService(prefix, self.port)

    def start(self):
        """
        Starts the command http server in a thread
        """
        web.run_app(self._app, port=self.port)
