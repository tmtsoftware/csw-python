import uuid

import requests

from csw.CommandResponse import SubmitResponse, Error, CommandResponse
from csw.CommandServiceRequest import Submit, Validate, Oneway
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.ParameterSetType import ControlCommand
from csw.Prefix import Prefix
import json
from dataclasses import dataclass


# A CSW command service client
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

    def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Submit", controlCommand)

    def validate(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Validate", controlCommand)

    def oneway(self, controlCommand: ControlCommand) -> SubmitResponse:
        return self._postCommand("Oneway", controlCommand)
