from typing import Callable

import structlog
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit
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
            self.scriptApi.execute(command)
        except Exception as err:
            raise web.HTTPBadRequest(text=f"execute: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeGoOnline(self, request: Request) -> Response:
        self.log.info(f"Received executeGoOnline sequence command")
        try:
            self.scriptApi.executeGoOnline()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeGoOnline: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeGoOffline(self, request: Request) -> Response:
        self.log.info(f"Received executeGoOffline sequence command")
        try:
            self.scriptApi.executeGoOffline()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeGoOffline: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeShutdown(self, request: Request) -> Response:
        self.log.info(f"Received executeShutdown sequence command")
        try:
            self.scriptApi.executeShutdown()
            self._regResult.unregister()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeShutdown: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeAbort(self, request: Request) -> Response:
        self.log.info(f"Received executeAbort sequence command")
        try:
            self.scriptApi.executeAbort()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeAbort: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeNewSequenceHandler(self, request: Request) -> Response:
        self.log.info(f"Received executeNewSequenceHandler sequence command")
        try:
            self.scriptApi.executeNewSequenceHandler()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeNewSequenceHandler: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeStop(self, request: Request) -> Response:
        self.log.info(f"Received executeStop sequence command")
        try:
            self.scriptApi.executeStop()
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
            self.scriptApi.executeDiagnosticMode(mode.startTime, mode.hint)
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeDiagnosticMode: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _executeOperationsMode(self, request: Request) -> Response:
        self.log.info(f"Received executeOperationsMode sequence command")
        try:
            self.log.info("XXXX 1")
            self.scriptApi.executeOperationsMode()
            self.log.info("XXXX 2")
        except Exception as err:
            self.log.info(f"XXX OcsScriptServer._executeOperationsMode exception: {err=}")
            raise web.HTTPBadRequest(text=f"executeOperationsMode: {err=}, {type(err)=}")
        self.log.info(f"XXX OcsScriptServer._executeOperationsMode OK")
        return web.HTTPOk()

    async def _executeExceptionHandlers(self, request: Request) -> Response:
        self.log.info(f"Received executeExceptionHandlers sequence command")
        try:
            self.scriptApi.executeExceptionHandlers(Exception("XXX TODO"))
        except Exception as err:
            raise web.HTTPBadRequest(text=f"executeExceptionHandlers: {err=}, {type(err)=}")
        return web.HTTPOk()

    async def _shutdownScript(self, request: Request) -> Response:
        self.log.info(f"Received shutdownScript sequence command")
        try:
            self.scriptApi.shutdownScript()
        except Exception as err:
            raise web.HTTPBadRequest(text=f"shutdownScript: {err=}, {type(err)=}")
        await self._app.shutdown()
        return web.HTTPOk()

    @staticmethod
    def _registerWithLocationService(prefix: Prefix, port: int) -> RegistrationResult:
        locationService = LocationService()
        connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
        atexit.register(locationService.unregister, connection)
        return locationService.register(HttpRegistration(connection, port))

    def __init__(self, scriptApi: ScriptApi, sequencerPrefix: Prefix, sequenceComponentPrefix: Prefix, port: int = 0):
        """
        Creates an HTTP server that can dynamically load python sequencer scripts

        Args:
            scriptApi (ScriptApi): implements the script API
            sequencerPrefix (str): a CSW Prefix for the sequencer in the format $subsystem.name
            sequenceComponentPrefix (str): the ESW sequencer component prefix
            port (int): optional port for HTTP server
        """
        self._app = web.Application()
        self._crm = CommandResponseManager()
        self.log = structlog.get_logger()
        self.sequencerPrefix = sequencerPrefix
        self.sequenceComponentPrefix = sequenceComponentPrefix
        self.port = LocationService.getFreePort(port)
        self.scriptApi = scriptApi
        self._app.add_routes([
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
        self._regResult =  OcsScriptServer._registerWithLocationService(sequencerPrefix, self.port)

    def start(self):
        """
        Starts the command http server in a thread
        """
        web.run_app(self._app, port=self.port)


def main():
    if len(sys.argv) != 3:
        print("Expected two args: sequencerPrefix and sequenceComponentPrefix")
        sys.exit(1)

    sequencerPrefix = Prefix.from_str(sys.argv[1])
    sequenceComponentPrefix = Prefix.from_str(sys.argv[2])
    sequencerApi: SequencerApi = SequencerClient(sequencerPrefix)
    sequenceOperatorFactory: Callable[[], SequenceOperatorHttp] = lambda: SequenceOperatorHttp(sequencerApi)
    obsMode = ObsMode.fromPrefix(sequencerPrefix)
    evenService = EventService()
    alarmService = AlarmService()
    scriptContext = ScriptContext(1, sequencerPrefix, obsMode, sequenceOperatorFactory, evenService, alarmService)
    scriptWiring = ScriptWiring(scriptContext)
    script = Script(scriptWiring)
    # XXX TODO FIXME
    cfg = configparser.ConfigParser()
    # TODO FIXME: how to set this path?
    cfg.read('/shared/work/tmt/csw/pycsw/sequencer/examples/examples.ini')
    scriptFile = cfg.get("scripts", str(sequencerPrefix))
    module = ScriptLoader.loadPythonScript(scriptFile)
    module.script(script)
    scriptServer = OcsScriptServer(script.scriptDsl, sequencerPrefix, sequenceComponentPrefix)
    print(f"Starting script server on port {scriptServer.port}")
    scriptServer.start()


if __name__ == "__main__":
    main()
