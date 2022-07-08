import uuid

import requests

from csw.CommandResponse import SubmitResponse, Error, CommandResponse
from csw.CommandServiceRequest import Submit
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
        location.__class__ = HttpLocation
        return location.uri

    def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        # wsUri = f"{baseUri}websocket-endpoint"
        headers = {'Content-type': 'application/json'}
        data = Submit(controlCommand)._asDict()
        jsonStr = json.loads(json.dumps(data))
        response = requests.post(postUri, headers=headers, json=jsonStr)
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, response.text)
        resp = CommandResponse._fromDict(response.json())
        return resp
