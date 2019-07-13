import socketserver
from http.server import BaseHTTPRequestHandler
import json

from csw.CommandResponse import SubmitResponse
from csw.ControlCommand import ControlCommand
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType


class CommandHandler(BaseHTTPRequestHandler):
    """
    Abstract base class for handling CSW commands.
    Subclasses should override onSubmit() and/or onOneway() to implement the behavior for those commands.
    """

    def do_GET(self):
        self.send_response(400)

    def do_HEAD(self):
        self.send_response(400)

    def onSubmit(self, setup: ControlCommand) -> SubmitResponse:
        pass

    def onOneway(self, setup: ControlCommand):
        pass

    def do_POST(self):
        contentLength = int(self.headers['Content-Length'])
        data = self.rfile.read(contentLength)
        command = ControlCommand.fromDict(json.loads(data), flat=True)

        if self.path.endswith('/submit'):
            commandResponse = self.onSubmit(command)
            responseDict = commandResponse.asDict(flat=True)
            responseData = json.dumps(responseDict)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(responseData.encode())
        else:
            self.onOneway(command)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()


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
