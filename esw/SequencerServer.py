import json

import aiohttp
from aiohttp import web, WSMessage
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit

from aiohttp.web_ws import WebSocketResponse

from csw.CommandResponseManager import CommandResponseManager
from csw.CommandServer import QueryFinal, SubscribeCurrentState
from csw.ComponentHandlers import ComponentHandlers
from csw.Prefix import Prefix
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration
import structlog
from esw.SequencerRequest import LoadSequence, StartSequence
from esw.SequencerRequest import SequencerRequest


# Ignore generated functions in API docs
__pdoc__ = {}

log = structlog.get_logger()


class SequencerServer:
    _app = web.Application()
    _crm = CommandResponseManager()

    async def _handlePost(self, request: Request) -> Response:
        obj = await request.json()
        # log.debug(f"received post: {str(obj)}")

        match SequencerRequest._fromDict(obj):
            case LoadSequence(sequence):
                pass
            case StartSequence():
                pass
            # case 'GetSequence':
            #     pass
            # case 'Add':
            #     pass
            # case 'Prepend':
            #     pass
            # case 'Replace':
            #     pass
            # case 'InsertAfter':
            #     pass
            # case 'Delete':
            #     pass
            # case 'Pause':
            #     pass
            # case 'Resume':
            #     pass
            # case 'AddBreakpoint':
            #     pass
            # case 'RemoveBreakpoint':
            #     pass
            # case 'Reset':
            #     pass
            # case 'AbortSequence':
            #     pass
            # case 'Stop':
            #     pass
            # case 'Submit':
            #     pass
            # case 'Query':
            #     pass
            # case 'GoOnline':
            #     pass
            # case 'GoOffline':
            #     pass
            # case 'DiagnosticMode':
            #     pass
            # case 'OperationsMode':
            #     pass
            # case 'GetSequenceComponent':
            #     pass
            # case 'GetSequencerState':
            #     pass

        # if method in {'Submit', 'Oneway', 'Validate'}:
        #     command = ControlCommand._fromDict(obj['controlCommand'])
        #     runId = str(uuid.uuid4())
        #     if method == 'Submit':
        #         commandResponse, task = self.handler.onSubmit(runId, command)
        #         if task is not None:
        #             # noinspection PyTypeChecker
        #             self._crm.addTask(runId, task)
        #             log.debug("Long running task in progress...")
        #     elif method == 'Oneway':
        #         commandResponse = self.handler.onOneway(runId, command)
        #     else:
        #         commandResponse = self.handler.validateCommand(runId, command)
        #     responseDict = commandResponse._asDict()
        #     return web.json_response(responseDict)
        # else:
        #     raise Exception("Invalid command type: " + method)

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
                    log.debug("Received ws close message")
                    await ws.close()
                else:
                    obj = json.loads(msg.data)
                    # log.debug(f"received message: {str(obj)}")
                    method = obj['_type']
                    if method == "QueryFinal":
                        queryFinal = QueryFinal._fromDict(obj)
                        resp = await self._handleQueryFinal(queryFinal)
                        await ws.send_str(resp.text)
                        await ws.close()
                    elif method == "SubscribeCurrentState":
                        stateNames = SubscribeCurrentState._fromDict(obj).stateNames
                        log.debug(f"Received SubscribeCurrentState: stateNames = {stateNames}")
                        self.handler._subscribeCurrentState(stateNames, ws)
                    else:
                        log.debug(f"Warning: Received unknown ws message: {str(msg.data)}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                log.debug('Error: ws connection closed with exception %s' % ws.exception())
        log.debug('websocket connection closed')
        self.handler._unsubscribeCurrentState(ws)
        return ws

    @staticmethod
    def _registerWithLocationService(prefix: Prefix, port: int):
        log.debug("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
        atexit.register(locationService.unregister, connection)
        # locationService.unregister(connection)
        locationService.register(HttpRegistration(connection, port, "/post-endpoint"))

    def __init__(self, prefix: Prefix, handler: ComponentHandlers, port: int = 8082):
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
