import socketserver
from http.server import BaseHTTPRequestHandler
from cbor2 import *

from csw.CommandResponse import SubmitResponse
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType
from csw.Setup import Setup


class CommandHandler(BaseHTTPRequestHandler):
    """
    Abstract base class for handling CSW commands.
    Subclasses should override onSubmit() and/or onOneway() to implement the behavior for those commands.
    """

    def do_GET(self):
        self.send_response(400)

    def do_HEAD(self):
        self.send_response(400)

    def onSubmit(self, setup: Setup) -> SubmitResponse:
        pass

    def onOneway(self, setup: Setup):
        pass

    def do_POST(self):
        contentLength = int(self.headers['Content-Length'])
        data = self.rfile.read(contentLength)
        setup = Setup.fromDict(loads(data))

        if self.path == '/submit':
            commandResponse = self.onSubmit(setup)
            responseDict = {str(commandResponse.__class__.__name__): commandResponse.asDict()}
            responseData = dumps(responseDict)
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(responseData)
        else:
            self.onOneway(setup)
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()


class CommandServer:
    """
    Creates an HTTP server that can receive CSW Setup commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.

    Test with curl example:
        curl -d @./command.cbor -v -H "Content-Type: application/octet-stream" http://localhost:8082/submit
        or: curl -d @./command.cbor -v -H "Content-Type: application/octet-stream" http://localhost:8082/oneway
    """

    def __init__(self, name: str, handler: CommandHandler, port: int = 8082):
        locationService = LocationService()
        connection = ConnectionInfo(name, ComponentType.Service.value, ConnectionType.HttpType.value)
        reg = Registration(port, connection)
        locationService.register(RegType.HttpRegistration, reg)

        with socketserver.TCPServer(("", port), handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()
