import uuid
import requests
import websockets

from csw.CommandResponse import SubmitResponse, Error, CommandResponse
from csw.CommandServiceRequest import Submit, Validate, Oneway, QueryFinal
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
import json
from dataclasses import dataclass


# A CSW command service client
# noinspection PyProtectedMember
@dataclass
class CommandService:
    prefix: Prefix
    componentType: ComponentType

    def _getBaseUri(self) -> str:
        locationService = LocationService()
        connection = ConnectionInfo.make(self.prefix, self.componentType, ConnectionType.HttpType)
        location = locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    def _postCommand(self, command: str, controlCommand: ControlCommand) -> SubmitResponse:
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        match command:
            case 'Submit':
                data = Submit(controlCommand)._asDict()
            case 'Validate':
                data = Validate(controlCommand)._asDict()
            case _:
                data = Oneway(controlCommand)._asDict()
        jsonStr = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonStr)
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, response.text)
        resp = CommandResponse._fromDict(response.json())
        return resp

    # def _wsCommand(self, command: str, controlCommand: ControlCommand) -> SubmitResponse:
    #     baseUri = self._getBaseUri()
    #     wsUri = f"{baseUri}websocket-endpoint"
    #     match command:
    #         case 'QueryFinal': pass

    def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Submit", controlCommand)

    def validate(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Validate", controlCommand)

    def oneway(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Oneway", controlCommand)

    async def queryFinal(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        respDict = QueryFinal(runId, timeoutInSeconds)._asDict()
        jsonStr = json.dumps(respDict)
        async with websockets.connect(wsUri) as websocket:
            await websocket.send(jsonStr)
            jsonResp = await websocket.recv()
            return CommandResponse._fromDict(json.loads(jsonResp))



