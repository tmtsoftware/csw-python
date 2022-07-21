import json
from websocket import create_connection

import requests
from requests import Response

from csw.CommandResponse import SubmitResponse, CommandResponse, Started
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from esw.Sequence import Sequence
from esw.SequencerRequest import *
from esw.SequencerRes import *
from esw.StepList import StepList

# noinspection PyProtectedMember,PyShadowingBuiltins
from esw.WsCommands import QueryFinal


# noinspection DuplicatedCode,PyShadowingBuiltins
@dataclass
class SequencerClient:
    prefix: Prefix

    def _getBaseUri(self) -> str:
        locationService = LocationService()
        connection = ConnectionInfo.make(self.prefix, ComponentType.Sequencer, ConnectionType.HttpType)
        location = locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    def _postCommand(self, data: dict) -> Response:
        baseUri = self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        jsonData = json.loads(json.dumps(data))
        return requests.post(postUri, headers=headers, json=jsonData)

    def _postCommandGetResponse(self, request: SequencerRequest) -> SequencerRes:
        response = self._postCommand(request._asDict())
        if not response.ok:
            return Unhandled("Unknown", request.__class__.__name__, f"Error: {response.text}")
        return SequencerRes._fromDict(response.json())

    def getSequence(self) -> StepList | None:
        response = self._postCommand(GetSequence()._asDict())
        if not response.ok:
            return None
        return StepList._fromDict(response.json())

    def isAvailable(self) -> bool:
        response = self._postCommand(IsAvailable()._asDict())
        if not response.ok:
            return False
        return response.json()

    def isOnline(self) -> bool:
        response = self._postCommand(IsOnline()._asDict())
        if not response.ok:
            return False
        return response.json()

    def add(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(Add(commands))

    def prepend(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(Prepend(commands))

    def replace(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        return self._postCommandGetResponse(Replace(id, commands))

    def insertAfter(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        return self._postCommandGetResponse(InsertAfter(id, commands))

    def delete(self, id: str) -> GenericResponse:
        return self._postCommandGetResponse(Delete(id))

    def pause(self) -> PauseResponse:
        return self._postCommandGetResponse(Pause())

    def resume(self) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(Resume())

    def addBreakpoint(self, id: str) -> GenericResponse:
        return self._postCommandGetResponse(AddBreakpoint(id))

    def removeBreakpoint(self, id: str) -> GenericResponse:
        return self._postCommandGetResponse(RemoveBreakpoint(id))

    def reset(self) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(Reset())

    def abortSequence(self) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(AbortSequence())

    def stop(self) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(Stop())

    # --- commandApi ---

    def loadSequence(self, sequence: Sequence) -> OkOrUnhandledResponse:
        return self._postCommandGetResponse(LoadSequence(sequence.commands))

    def startSequence(self) -> SubmitResponse:
        return self._postCommandGetResponse(StartSequence())

    def submit(self, sequence: Sequence) -> SubmitResponse:
        return self._postCommandGetResponse(Submit(sequence.commands))

    def query(self, id: str) -> SubmitResponse:
        return self._postCommandGetResponse(Query(id))

    def queryFinal(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        respDict = QueryFinal(runId, timeoutInSeconds)._asDict()
        jsonStr = json.dumps(respDict)
        ws = create_connection(wsUri)
        ws.send(jsonStr)
        jsonResp = ws.recv()
        return CommandResponse._fromDict(json.loads(jsonResp))

    def submitAndWait(self, sequence: Sequence, timeoutInSeconds: int) -> SubmitResponse:
        resp = self.submit(sequence)
        match resp:
            case Started(runId):
                return self.queryFinal(runId, timeoutInSeconds)
            case _:
                return resp

    def goOnline(self) -> GoOnlineResponse:
        return self._postCommandGetResponse(GoOnline())

    def goOffline(self) -> GoOfflineResponse:
        return self._postCommandGetResponse(GoOffline())

    def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        return self._postCommandGetResponse(DiagnosticMode(startTime, hint))

    def operationsMode(self) -> OperationsModeResponse:
        return self._postCommandGetResponse(OperationsMode())

    def getSequencerState(self) -> SequencerState:
        response = self._postCommand(GetSequencerState()._asDict())
        if not response.ok:
            return SequencerState.Offline
        match response.json()["_type"]:
            case "Idle":
                return SequencerState.Idle
            case "Processing":
                return SequencerState.Processing
            case "Loaded":
                return SequencerState.Loaded
            case "Offline":
                return SequencerState.Offline
            case "Running":
                return SequencerState.Running

    # def subscribeSequencerState(self):
    #     xxx websocket ... = SubscribeSequencerState()
