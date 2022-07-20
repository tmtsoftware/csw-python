import json
from dataclasses import dataclass

import requests
from requests import Response

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from esw.SequencerRequest import GetSequence
from esw.StepList import StepList


# noinspection PyProtectedMember
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


    def getSequence(self) -> StepList | None:
        response = self._postCommand(GetSequence()._asDict())
        if not response.ok:
            return None
        return StepList._fromDict(response.json())


#     override def isAvailable: Future[Boolean] = postClient.requestResponse[Boolean](IsAvailable)
#
#     override def isOnline: Future[Boolean] = postClient.requestResponse[Boolean](IsOnline)
#
#     override def add(commands: List[SequenceCommand]): Future[OkOrUnhandledResponse] =
#     postClient.requestResponse[OkOrUnhandledResponse](Add(commands))
#
# override def prepend(commands: List[SequenceCommand]): Future[OkOrUnhandledResponse] =
# postClient.requestResponse[OkOrUnhandledResponse](Prepend(commands))
#
# override def replace(id: Id, commands: List[SequenceCommand]): Future[GenericResponse] =
# postClient.requestResponse[GenericResponse](Replace(id, commands))
#
# override def insertAfter(id: Id, commands: List[SequenceCommand]): Future[GenericResponse] =
# postClient.requestResponse[GenericResponse](InsertAfter(id, commands))
#
# override def delete(id: Id): Future[GenericResponse] = postClient.requestResponse[GenericResponse](Delete(id))
#
# override def pause: Future[PauseResponse] = {
#     postClient.requestResponse[PauseResponse](Pause)
# }
#
# override def resume: Future[OkOrUnhandledResponse] = postClient.requestResponse[OkOrUnhandledResponse](Resume)
#
# override def addBreakpoint(id: Id): Future[GenericResponse] =
# postClient.requestResponse[GenericResponse](AddBreakpoint(id))
#
# override def removeBreakpoint(id: Id): Future[RemoveBreakpointResponse] =
# postClient.requestResponse[RemoveBreakpointResponse](RemoveBreakpoint(id))
#
# override def reset(): Future[OkOrUnhandledResponse] = postClient.requestResponse[OkOrUnhandledResponse](Reset)
#
# override def abortSequence(): Future[OkOrUnhandledResponse] =
# postClient.requestResponse[OkOrUnhandledResponse](AbortSequence)
#
# override def stop(): Future[OkOrUnhandledResponse] =
# postClient.requestResponse[OkOrUnhandledResponse](Stop)
#
# // commandApi
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
