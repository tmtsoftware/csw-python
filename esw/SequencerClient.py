import json
from dataclasses import dataclass

import requests
from requests import Response

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from esw.Sequence import Sequence
from esw.SequencerRequest import *
from esw.SequencerRes import *
from esw.StepList import StepList


# noinspection PyProtectedMember,PyShadowingBuiltins
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

# override def loadSequence(sequence: Sequence): Future[OkOrUnhandledResponse] =
# postClient.requestResponse[OkOrUnhandledResponse](LoadSequence(sequence))
#
# override def startSequence(): Future[SubmitResponse] = postClient.requestResponse[SubmitResponse](StartSequence)
#
# override def submit(sequence: Sequence): Future[SubmitResponse] =
# postClient.requestResponse[SubmitResponse](Submit(sequence))
#
# override def submitAndWait(sequence: Sequence)(implicit timeout: Timeout): Future[SubmitResponse] =
# extensions.submitAndWait(sequence)
#
# override def query(runId: Id): Future[SubmitResponse] =
# postClient.requestResponse[SubmitResponse](Query(runId))
#
# override def queryFinal(runId: Id)(implicit timeout: Timeout): Future[SubmitResponse] =
# websocketClient.requestResponse[SubmitResponse](QueryFinal(runId, timeout), timeout.duration)
#
# override def goOnline(): Future[GoOnlineResponse] = postClient.requestResponse[GoOnlineResponse](GoOnline)
#
# override def goOffline(): Future[GoOfflineResponse] = postClient.requestResponse[GoOfflineResponse](GoOffline)
#
# override def diagnosticMode(startTime: UTCTime, hint: String): Future[DiagnosticModeResponse] =
# postClient.requestResponse[DiagnosticModeResponse](DiagnosticMode(startTime, hint))
#
# override def operationsMode(): Future[OperationsModeResponse] =
# postClient.requestResponse[OperationsModeResponse](OperationsMode)
#
# override def getSequenceComponent: Future[AkkaLocation] = postClient.requestResponse[AkkaLocation](GetSequenceComponent)
#
# override def getSequencerState: Future[SequencerState] =
# postClient.requestResponse[SequencerState](GetSequencerState)
#
# override def subscribeSequencerState(): Source[SequencerStateResponse, Subscription] =
# websocketClient.requestStream[SequencerStateResponse](SubscribeSequencerState)
