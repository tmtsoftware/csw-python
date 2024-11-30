import os
import traceback
from typing import Callable

import asyncio_atexit

import structlog
from aiohttp import web, ClientSession
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import sys
import configparser

from csw.AlarmService import AlarmService
from csw.CommandResponseManager import CommandResponseManager
from csw.EventService import EventService
from csw.ParameterSetType import SequenceCommand
from csw.Prefix import Prefix
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration, \
    RegistrationResult
from esw.ObsMode import ObsMode
from esw.SequencerClient import SequencerClient
from esw.SequencerRequest import DiagnosticMode
from sequencer.CswServices import CswServices
from sequencer.Script import Script
from sequencer.ScriptApi import ScriptApi
from sequencer.ScriptContext import ScriptContext
from sequencer.ScriptLoader import ScriptLoader
from sequencer.ScriptWiring import ScriptWiring
from sequencer.SequenceOperatorApi import SequenceOperatorHttp
from sequencer.SequencerApi import SequencerApi


# noinspection PyPep8Naming,PyUnusedLocal
class OcsScriptServer:
    async def _execute(self, request: Request) -> Response:
        obj = await request.json()
        try:
            command: SequenceCommand = SequenceCommand._fromDict(obj)
        except TypeError:
            raise web.HTTPBadRequest(text='Bad request')
        self.log.info(f"Received execute sequence command: {command}")
        try:
            await self.scriptApi.execute(command)
        except Exception as err:
            raise web.HTTPBadRequest(text=f"execute: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeGoOnline(self, request: Request) -> Response:
        self.log.info(f"Received executeGoOnline sequence command")
        try:
            await self.scriptApi.executeGoOnline()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeGoOnline: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeGoOffline(self, request: Request) -> Response:
        self.log.info(f"Received executeGoOffline sequence command")
        try:
            await self.scriptApi.executeGoOffline()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeGoOffline: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeShutdown(self, request: Request) -> Response:
        self.log.info(f"Received executeShutdown sequence command")
        try:
            await self.scriptApi.executeShutdown()
            self._regResult.unregister()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeShutdown: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeAbort(self, request: Request) -> Response:
        self.log.info(f"Received executeAbort sequence command")
        try:
            await self.scriptApi.executeAbort()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeAbort: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeNewSequenceHandler(self, request: Request) -> Response:
        self.log.info(f"Received executeNewSequenceHandler sequence command")
        try:
            await self.scriptApi.executeNewSequenceHandler()
        except Exception as err:
            self.log.error(f"executeNewSequenceHandler: {err=}, {type(err)=}")
            traceback.print_exc()
            raise web.HTTPBadRequest(text=f"executeNewSequenceHandler: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeStop(self, request: Request) -> Response:
        self.log.info(f"Received executeStop sequence command")
        try:
            await self.scriptApi.executeStop()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeStop: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeDiagnosticMode(self, request: Request) -> Response:
        obj = await request.json()
        try:
            mode: DiagnosticMode = DiagnosticMode._fromDict(obj)
        except TypeError:
            raise web.HTTPBadRequest(text='Bad request')
        self.log.info(f"Received executeDiagnosticMode sequence command: {mode}")
        try:
            await self.scriptApi.executeDiagnosticMode(mode.startTime, mode.hint)
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeDiagnosticMode: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeOperationsMode(self, request: Request) -> Response:
        self.log.info(f"Received executeOperationsMode sequence command")
        try:
            await self.scriptApi.executeOperationsMode()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeOperationsMode: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeExceptionHandlers(self, request: Request) -> Response:
        try:
            await self.scriptApi.executeExceptionHandlers(Exception("XXX TODO"))
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeExceptionHandlers: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _shutdownScript(self, request: Request) -> Response:
        self.log.info(f"Received shutdownScript sequence command")
        try:
            await self.scriptApi.shutdownScript()
        except Exception as err:
            self.log.error(f"shutdownScript: {err=}, {type(err)=}")
            raise web.HTTPBadRequest(text=f"shutdownScript: {err=}, {type(err)=}")
        await self.app.shutdown()
        return web.HTTPOk()

    async def _registerWithLocationService(self) -> RegistrationResult:
        locationService = LocationService(self.clientSession)
        connection = ConnectionInfo.make(self.sequencerPrefix, ComponentType.Service, ConnectionType.HttpType)
        async def unreg():
            await locationService.unregister(connection)
        asyncio_atexit.register(unreg)
        return await locationService.register(HttpRegistration(connection, self.port))

    def __init__(self):
        self.clientSession = ClientSession()
        self._crm = CommandResponseManager()
        self.log = structlog.get_logger()
        self.sequencerPrefix = Prefix.from_str(sys.argv[1])
        self.sequenceComponentPrefix = Prefix.from_str(sys.argv[2])
        self.port = LocationService.getFreePort(0)

    # We have to do all this initialization here, in order to be able have ClientSession share the event loop
    # with the server
    # See https://stackoverflow.com/questions/55963155/what-is-the-proper-way-to-use-clientsession-inside-aiohttp-web-server
    async def _clientSessionCtx(self, app: web.Application):
        sequencerApi: SequencerApi = SequencerClient(self.sequencerPrefix, self.clientSession)
        sequenceOperatorFactory: Callable[[], SequenceOperatorHttp] = lambda: SequenceOperatorHttp(sequencerApi)
        obsMode = ObsMode.fromPrefix(self.sequencerPrefix)
        evenService = EventService()
        alarmService = AlarmService()
        scriptContext = ScriptContext(1, self.sequencerPrefix, obsMode, self.clientSession, sequenceOperatorFactory,
                                      evenService,
                                      alarmService)
        cswServices = await CswServices.create(self.clientSession, scriptContext)
        scriptWiring = ScriptWiring(scriptContext, cswServices)
        script = Script(scriptWiring)
        self.scriptApi: ScriptApi = script.scriptDsl
        cfg = configparser.ConfigParser()
        thisDir = os.path.dirname(os.path.abspath(__file__))
        # XXX TODO FIXME: pass the location of the config file as an argument? Or use environment variable?
        cfg.read(f'{thisDir}/examples/examples.ini')
        scriptPath = cfg.get("scripts", str(self.sequencerPrefix))
        # Environment variable CSW_PYTHON_SCRIPT_DIR can override directory containing scripts
        # (the config file contains the relative paths)
        scriptDir = os.environ.get('CSW_PYTHON_SCRIPT_DIR', thisDir)
        scriptFile = f"{scriptDir}/{scriptPath}"
        module = ScriptLoader.loadPythonScript(scriptFile)
        module.script(script)
        print(f"Starting script server for {self.sequencerPrefix} ({scriptFile}) on port {self.port}")
        yield
        await self.clientSession.close()

    async def _appFactory(self) -> web.Application:
        self._regResult = await self._registerWithLocationService()
        self.app = web.Application()
        self.app.add_routes([
            web.post('/execute', self._execute),
            web.post('/executeGoOnline', self._executeGoOnline),
            web.post('/executeGoOffline', self._executeGoOffline),
            web.post('/executeShutdown', self._executeShutdown),
            web.post('/executeAbort', self._executeAbort),
            web.post('/executeNewSequenceHandler', self._executeNewSequenceHandler),
            web.post('/executeStop', self._executeStop),
            web.post('/executeDiagnosticMode', self._executeDiagnosticMode),
            web.post('/executeOperationsMode', self._executeOperationsMode),
            web.post('/executeExceptionHandlers', self._executeExceptionHandlers),
            web.post('/shutdownScript', self._shutdownScript)
        ])
        # Needed to have ClientSession and server share the asyncio event loop
        self.app.cleanup_ctx.append(self._clientSessionCtx)
        return self.app

    def start(self):
        """
        Starts the command http server in a thread
        """
        web.run_app(self._appFactory(), port=self.port)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Expected two args: sequencerPrefix and sequenceComponentPrefix")
        sys.exit(1)
    OcsScriptServer().start()
