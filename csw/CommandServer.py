from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit

from csw.CommandResponseManager import CommandResponseManager
from csw.ComponentHandlers import ComponentHandlers
from csw.ControlCommand import ControlCommand
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpRegistration, \
    RegType, Prefix


class CommandServer:
    """
    Creates an HTTP server that can receive CSW commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.
    """

    crm = CommandResponseManager()

    async def _handleCommand(self, request: Request) -> Response:
        print("XXX handleCommand: request = " + str(request))
        method = request.match_info['method']
        if method in {'submit', 'oneway', 'validate'}:
            data = await request.json()
            command = ControlCommand.fromDict(data)
            if method == 'submit':
                commandResponse, task = self.handler.onSubmit(command)
                if task is not None:
                    # noinspection PyTypeChecker
                    self.crm.addTask(command.runId, task)
                    print("A task is still running")
            elif method == 'oneway':
                commandResponse = self.handler.onOneway(command)
            else:
                commandResponse = self.handler.validateCommand(command)
            responseDict = commandResponse.asDict()
            return web.json_response(responseDict)
        else:
            raise web.HTTPBadRequest()

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
        locationService.register(HttpRegistration(connection, port, ""))

    def __init__(self, prefix: str, handler: ComponentHandlers, port: int = 8082):
        self.handler = handler
        app = web.Application()
        app.add_routes([
            web.post('/command/{componentType}/{componentName}/{method}', self._handleCommand),
            web.get('/command/{componentType}/{componentName}/{runId}', self._handleQueryFinal)
        ])

        self._registerWithLocationService(prefix, port)
        web.run_app(app, port=port)
