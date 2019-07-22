from asyncio import Task

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import atexit

from csw.CommandResponseManager import CommandResponseManager
from csw.ControlCommand import ControlCommand
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType
from csw.CommandResponse import CommandResponse, Accepted, Error


class ComponentHandlers:
    """
    Abstract base class for handling CSW commands.
    Subclasses can override methods to implement the behavior of the component.
    """

    def onSubmit(self, command: ControlCommand) -> (CommandResponse, Task):
        """
        Handles the given setup command and returns a CommandResponse subclass
        :param command: contains the command
        :return: a pair: (subclass of CommandResponse, Task),
        where the task can be None if the command response is final.
        For long running commands, you can respond with Started(runId, "...") and a task that
        completes the work in the background.
        """
        return Error(command.runId, "Not implemented: submit command handler"), None

    def onOneway(self, command: ControlCommand) -> CommandResponse:
        """
        Handles the given setup command and returns an immediate CommandResponse
        :param command: contains the command
        :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        return Error(command.runId, "Not implemented: oneway command handler")

    def validateCommand(self, command: ControlCommand) -> CommandResponse:
        """
       Validates the given command
       :param command: contains the command
       :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
       """
        return Accepted(command.runId)


class CommandServer:
    """
    Creates an HTTP server that can receive CSW commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.
    """

    crm = CommandResponseManager()

    async def _handleCommand(self, request: Request) -> Response:
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
        print("XXXX query final " + runId)
        commandResponse = await self.crm.waitForTask(runId)
        print("XXX result of long running command after await: " + str(commandResponse))
        responseDict = commandResponse.asDict()
        return web.json_response(responseDict)

    async def _handleSubscribeCurrentState(self, request: Request) -> Response:
        # TODO: subscribe to current state, respond with SSE connection
        raise web.HTTPBadRequest()

    @staticmethod
    def _registerWithLocationService(name: str, port: int):
        print("Registering with location service using port " + str(port))
        locationService = LocationService()
        connection = ConnectionInfo(name, ComponentType.Service.value, ConnectionType.HttpType.value)
        reg = Registration(port, connection)
        atexit.register(locationService.unregister, connection)
        locationService.register(RegType.HttpRegistration, reg)

    def __init__(self, name: str, handler: ComponentHandlers, port: int = 8082):
        self.handler = handler
        app = web.Application()
        app.add_routes([
            web.post('/command/{componentType}/{componentName}/{method}', self._handleCommand),
            web.get('/command/{componentType}/{componentName}/{runId}', self._handleQueryFinal),
            web.get('/command/{componentType}/{componentName}/current-state/subscribe',
                    self._handleSubscribeCurrentState)
        ])

        self._registerWithLocationService(name, port)
        web.run_app(app, port=port)
