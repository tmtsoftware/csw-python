from dataclasses import dataclass

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit
import uuid

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
class Query:
    runId: str


class CommandServer:
    """
    Creates an HTTP server that can receive CSW commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.
    """
    crm = CommandResponseManager()

    async def _handleCommand(self, request: Request) -> Response:
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
        elif method == 'Query':
            pass  # XXX TODO FIXME
        else:
            raise Exception("Invalid Location type: " + method)

    async def _handleQueryFinal(self, request: Request) -> Response:
        runId = request.match_info['runId']
        commandResponse = await self.crm.waitForTask(runId)
        responseDict = commandResponse.asDict()
        return web.json_response(responseDict)

    @staticmethod
    def _registerWithLocationService(prefix: str, port: int):
        print("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo(prefix, ComponentType.Service.value, ConnectionType.HttpType.value)
        atexit.register(locationService.unregister, connection)
        locationService.register(HttpRegistration(connection, port, "/post-endpoint"))

    def __init__(self, prefix: str, handler: ComponentHandlers, port: int = 8082):
        self.handler = handler
        app = web.Application()
        app.add_routes([
            web.post('/post-endpoint', self._handleCommand)
        ])
        self._registerWithLocationService(prefix, port)
        web.run_app(app, port=port)
