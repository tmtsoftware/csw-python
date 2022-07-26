import json
import uuid

import aiohttp
from aiohttp import web, WSMessage
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit

from aiohttp.web_ws import WebSocketResponse

from csw.CommandResponse import Error
from csw.CommandResponseManager import CommandResponseManager
from csw.CommandServiceRequest import QueryFinal
from csw.Prefix import Prefix
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration
import structlog
from esw.SequencerRequest import *
from esw.SequencerRequest import SequencerRequest

# XXX This class is in progress, not implemented yet

# noinspection PyProtectedMember,PyShadowingBuiltins
class SequencerServer:
    _app = web.Application()
    _crm = CommandResponseManager()

    log = structlog.get_logger()

    async def _handlePost(self, request: Request) -> Response:
        obj = await request.json()
        self.log.debug(f"received post: {str(obj)}")

        match SequencerRequest._fromDict(obj):
            case LoadSequence(sequence):
                pass
            case StartSequence():
                pass
            case GetSequence():
                pass
            case Add(commands):
                pass
            case Prepend(commands):
                pass
            case Replace(id, commands):
                pass
            case InsertAfter(id, commands):
                pass
            case Delete(id):
                pass
            case Pause():
                pass
            case Resume():
                pass
            case AddBreakpoint(id):
                pass
            case RemoveBreakpoint(id):
                pass
            case Reset():
                pass
            case AbortSequence():
                pass
            case Stop():
                pass
            case Submit(sequence):
                pass
            case Query(runId):
                pass
            case GoOnline():
                pass
            case GoOffline():
                pass
            case DiagnosticMode(startTime, hint):
                pass
            case OperationsMode():
                pass
            case GetSequenceComponent():
                pass
            case GetSequencerState():
                pass

        # XXX FIXME
        runId = str(uuid.uuid4())
        commandResponse = Error(runId, "XXX Not impl")
        return web.json_response(commandResponse._asDict())

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
                    self.log.debug("Received ws close message")
                    await ws.close()
                else:
                    obj = json.loads(msg.data)
                    self.log.debug(f"XXX received sequencer ws message: {str(obj)}")
                    method = obj['_type']
                    if method == "QueryFinal":
                        queryFinal = QueryFinal._fromDict(obj)
                        resp = await self._handleQueryFinal(queryFinal)
                        await ws.send_str(resp.text)
                        await ws.close()
                    elif method == "SubscribeSequencerState":
                        self.log.debug(f"Received SubscribeSequencerState")
                        self._subscribeSequencerState(ws)
                    else:
                        self.log.debug(f"Warning: Received unknown ws message: {str(msg.data)}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self.log.debug('Error: ws connection closed with exception %s' % ws.exception())
        self.log.debug('websocket connection closed')
        self._unsubscribeSequencerState(ws)
        return ws

    # List of sequencer state  websocket subscribers
    _sequencerStateSubscribers = set()

    # async def publishSequencerStates(self):
    #     """
    #     Publish the sequencer state
    #     """
    #     ss = json.dumps(sequencerState._asDict())
    #     for ws in self._sequencerStateSubscribers:
    #         self.log.debug(f"Publishing sequencer state: {ss}")
    #         await ws.send_str(ss)

    def _subscribeSequencerState(self, ws: WebSocketResponse):
        """
        Internal method used to subscribe to sequencer state of this component.
        """
        self._sequencerStateSubscribers.add(ws)

    def _unsubscribeSequencerState(self, ws: WebSocketResponse):
        """
        Internal method used to unsubscribe a websocket from sequencer state events
        """
        if ws in self._sequencerStateSubscribers:
            self._sequencerStateSubscribers.remove(ws)

    def _registerWithLocationService(self, prefix: Prefix, port: int):
        self.log.debug("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo.make(prefix, ComponentType.SequenceComponent, ConnectionType.HttpType)
        atexit.register(locationService.unregister, connection)
        locationService.register(HttpRegistration(connection, port))

    # XXXXXXXXXXXX ? handler? port? args?
    def __init__(self, prefix: Prefix, port: int = 8082):
        """
        Creates an HTTP server that can receive sequencer commands and registers it with the Location Service using the
        given prefix, so that CSW components can locate it and send commands to it.

        Args:
            prefix (str): a CSW Prefix in the format subsystem.name, where subsystem is one of the upper case TMT
                          subsystem names and name is the name of the sequencer
            port (int): optional port for HTTP server
        """
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
