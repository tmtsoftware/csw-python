import http.server
import socketserver
from http.server import BaseHTTPRequestHandler
from cbor2 import *
from dataclasses import asdict

from csw.CommandResponse import Completed
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, Registration, RegType
from csw.Setup import Setup


class CommandHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(400)

    def do_HEAD(self):
        self.send_response(400)

    def do_POST(self):
        contentLength = int(self.headers['Content-Length'])
        data = self.rfile.read(contentLength)
        print(f"XXX received {contentLength} bytes")
        setup = Setup.fromDict(loads(data))
        print("XXX received setup: " + str(setup))
        # TODO: Call supplied function and return actual response
        commandResponse = Completed(setup.runId)
        commandDict = {"Completed": asdict(commandResponse)}
        responseData = dumps(commandDict)
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()
        self.wfile.write(responseData)


class CommandServer:
    """
    Creates an HTTP server that can receive CSW Setup commands and registers it with the Location Service,
    so that CSW components can locate it and send commands to it.

    Test with curl example:
        curl -d @./command.cbor -v -H "Content-Type: application/octet-stream" http://localhost:8082/submit
    """
    def __init__(self, name: str, port: int = 8082):
        handler = CommandHandler
        locationService = LocationService()
        connection = ConnectionInfo(name, ComponentType.Service.value, ConnectionType.HttpType.value)
        reg = Registration(port, connection)
        locationService.register(RegType.HttpRegistration, reg)

        with socketserver.TCPServer(("", port), handler) as httpd:
            print("serving at port", port)
            httpd.serve_forever()
