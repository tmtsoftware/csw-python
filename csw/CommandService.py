import uuid
import requests
import websockets

from csw.CommandResponse import SubmitResponse, Error, CommandResponse, Started
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
    #     baseUri = self._getBaseUri().replace('http:', 'ws:')
    #     wsUri = f"{baseUri}websocket-endpoint"

    def submit(self, controlCommand: ControlCommand) -> SubmitResponse:
        """
        Submits a command to the command service

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        return self._postCommand("Submit", controlCommand)

    def validate(self, controlCommand: ControlCommand) -> SubmitResponse:
        """
        Validates a command to be sent to the command service.
        Note that in the jvm CSW API the return value is a ValidateResponse.
        Since Python does not have traits, the return type is marked as SubmitResponse.

        Args:
            controlCommand (ControlCommand): command to submit

        Returns: SubmitResponse
            a subclass of SubmitResponse (only Accepted, Invalid or Locked)
       """
        return self._postCommand("Validate", controlCommand)

    def oneway(self, controlCommand: ControlCommand) -> SubmitResponse:
        """
       Sends a command to the command service without expecting a reply.
       Note that in the jvm CSW API the return value is a OnewayResponse.
       Since Python does not have traits, the return type is marked as SubmitResponse.

       Args:
           controlCommand (ControlCommand): command to submit

       Returns: SubmitResponse
           a subclass of SubmitResponse (only Accepted, Invalid or Locked)
      """
        return self._postCommand("Oneway", controlCommand)

    async def queryFinal(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        """
       If the command for runId returned Started (long running command), this will
       return the final result.

       Args:
           runId (str): runId for the command
           timeoutInSeconds (int): seconds to wait before returning an error

       Returns: SubmitResponse
           a subclass of SubmitResponse
      """
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        respDict = QueryFinal(runId, timeoutInSeconds)._asDict()
        jsonStr = json.dumps(respDict)
        async with websockets.connect(wsUri) as websocket:
            await websocket.send(jsonStr)
            jsonResp = await websocket.recv()
            return CommandResponse._fromDict(json.loads(jsonResp))

    async def submitAndWait(self, controlCommand: ControlCommand, timeoutInSeconds: int) -> SubmitResponse:
        """
        Submits a command to the command service and waits for the final response.

        Args:
            controlCommand (ControlCommand): command to submit
            timeoutInSeconds (int): seconds to wait before returning an error

        Returns: SubmitResponse
            a subclass of SubmitResponse
       """
        resp = self.submit(controlCommand)
        match resp:
            case Started(runId):
                return await self.queryFinal(runId, timeoutInSeconds)
            case _:
                return resp
