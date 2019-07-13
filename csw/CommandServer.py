import socketserver
from http.server import BaseHTTPRequestHandler
import json
import ntpath

from csw.CommandResponse import CommandResponse, Accepted
from csw.ControlCommand import ControlCommand
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType


class CommandHandler(BaseHTTPRequestHandler):
    """
    Abstract base class for handling CSW commands.
    Subclasses can override onSubmit() and/or onOneway() to implement the behavior for those commands.
    """

    def do_GET(self):
        self.send_response(400)

    def do_HEAD(self):
        self.send_response(400)

    def onSubmit(self, command: ControlCommand) -> CommandResponse:
        """
        Handles the given setup command and returns a CommandResponse subclass
        :param command: contains the command
        :return: a subclass of CommandResponse
        """
        pass

    def onOneway(self, command: ControlCommand) -> CommandResponse:
        """
        Handles the given setup command and returns an immediate CommandResponse
        :param command: contains the command
        :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
        """
        pass

    def validate(self, command: ControlCommand) -> CommandResponse:
        """
       Validates the given command
       :param command: contains the command
       :return: a subclass of CommandResponse (only Accepted, Invalid or Locked are allowed)
       """
        return Accepted(command.runId)

    def _handleCommand(self, method: str):
        contentLength = int(self.headers['Content-Length'])
        data = self.rfile.read(contentLength)
        command = ControlCommand.fromDict(json.loads(data), flat=True)
        if method == 'submit':
            commandResponse = self.onSubmit(command)
        elif method == 'oneway':
            commandResponse = self.onOneway(command)
        else:
            commandResponse = self.validate(command)
        responseDict = commandResponse.asDict(flat=True)
        responseData = json.dumps(responseDict)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(responseData.encode())

    def do_POST(self):
        method = ntpath.basename(self.path)
        if method in {'submit', 'oneway', 'validate'}:
            self._handleCommand(method)
        else:
            self.send_response(400)


class CommandServer:
    """
    Creates an HTTP server that can receive CSW Setup commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.
    """

    def __init__(self, name: str, handler: CommandHandler, port: int = 8082):
        locationService = LocationService()
        connection = ConnectionInfo(name, ComponentType.Service.value, ConnectionType.HttpType.value)
        reg = Registration(port, connection)
        locationService.register(RegType.HttpRegistration, reg)

        with socketserver.TCPServer(("", port), handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()
