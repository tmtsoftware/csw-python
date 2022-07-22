import json
import uuid

from websocket import create_connection
from dataclasses import dataclass

import requests
from requests import Response

from csw.CommandResponse import SubmitResponse, CommandResponse, Started, Error
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
        """
        Get the sequence in sequencer - current or last.
        If there is no sequence
        then None response is returned
        otherwise a StepList is returned.

        Returns: StepList
            a list of steps in the sequence
       """
        response = self._postCommand(GetSequence()._asDict())
        if not response.ok:
            return None
        return StepList._fromDict(response.json())

    def isAvailable(self) -> bool:
        """
        Checks if sequencer is in Idle state.

        Returns: bool
            true if the sequencer is available
       """
        response = self._postCommand(IsAvailable()._asDict())
        if not response.ok:
            return False
        return response.json()

    def isOnline(self) -> bool:
        """
        Checks if sequencer is in Online(any state except Offline) state

        Returns: bool
            true if the sequencer is online
       """
        response = self._postCommand(IsOnline()._asDict())
        if not response.ok:
            return False
        return response.json()

    def add(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        """
        Adds the given list of sequence commands at the end of the sequencee

        Args:
            commands (List[SequenceCommand]): list of SequenceCommand to add in the sequence of sequencer

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(Add(commands))

    def prepend(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        """
        Prepends the given list of sequence commands in the sequence

        Args:
            commands (List[SequenceCommand]): list of SequenceCommand to prepend in the sequence of sequencer

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(Prepend(commands))

    def replace(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        """
        Replaces the command of the given id with the given list of sequence commands in the sequence

        Args:
            id (str): runId of command which is to be replaced
            commands (List[SequenceCommand]): list of SequenceCommand to replace with

        Returns: GenericResponse
       """
        return self._postCommandGetResponse(Replace(id, commands))

    def insertAfter(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        """
        Inserts the given list of sequence commands after the command of given id in the sequence

        Args:
            id (str): runId of command after which the given list of commands is to be inserted
            commands (List[SequenceCommand]): list of SequenceCommand to be inserted

        Returns: GenericResponse
       """
        return self._postCommandGetResponse(InsertAfter(id, commands))

    def delete(self, id: str) -> GenericResponse:
        """
        Deletes the command of the given id in the sequence

        Args:
            id (str): runId of the command which is to be deleted

        Returns: GenericResponse
       """
        return self._postCommandGetResponse(Delete(id))

    def pause(self) -> PauseResponse:
        """
        Pauses the running sequence

        Returns: PauseResponse
       """
        return self._postCommandGetResponse(Pause())

    def resume(self) -> OkOrUnhandledResponse:
        """
        Resumes the paused sequence

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(Resume())

    def addBreakpoint(self, id: str) -> GenericResponse:
        """
        Adds a breakpoint at the command of the given id in the sequence

        Args:
            id (str): runId of the command where breakpoint is to be added

        Returns: GenericResponse
       """
        return self._postCommandGetResponse(AddBreakpoint(id))

    def removeBreakpoint(self, id: str) -> GenericResponse:
        """
       Removes a breakpoint from the command of the given id in the sequence

       Args:
           id (str): runId of command where breakpoint is set

       Returns: GenericResponse
      """
        return self._postCommandGetResponse(RemoveBreakpoint(id))

    def reset(self) -> OkOrUnhandledResponse:
        """
        Resets the sequence by discarding all the pending steps of the sequence

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(Reset())

    def abortSequence(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the abort handler of the sequencer's script

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(AbortSequence())

    def stop(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the stop handler of the sequencer's script

        Returns: OkOrUnhandledResponse
       """
        return self._postCommandGetResponse(Stop())

    # --- commandApi ---

    def loadSequence(self, sequence: Sequence) -> OkOrUnhandledResponse:
        """
        Loads the given sequence to the sequencer.
        If the sequencer is in Idle or Loaded state
        then Ok response is returned
        otherwise Unhandled response is returned

        Args:
           sequence (Sequence): sequence to run on the sequencer

        Returns: OkOrUnhandledResponse
      """
        return self._postCommandGetResponse(LoadSequence(sequence.commands))

    def startSequence(self) -> SubmitResponse:
        """
        Starts the loaded sequence in the sequencer.
        If the sequencer is loaded then a Started response is returned.
        If the sequencer is already running another sequence, an Invalid response is returned.

        Returns: SubmitResponse
            an initial SubmitResponse
       """
        return self._postCommandGetResponse(StartSequence())

    def submit(self, sequence: Sequence) -> SubmitResponse:
        """
        Submits the given sequence to the sequencer.
        If the sequencer is idle, the provided sequence is loaded in the sequencer and execution of the sequence
        starts immediately, and a Started response is returned.
        If the sequencer is already running another sequence, an Invalid response is returned.

        Args:
           sequence (Sequence): sequence to run on the sequencer

        Returns: SubmitResponse
            initial response
      """
        response = self._postCommand(Submit(sequence.commands)._asDict())
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, response.text)
        return CommandResponse._fromDict(response.json())

    def query(self, id: str) -> SubmitResponse:
        """
        Query for the result of the sequence which was submitted to get a SubmitResponse.
        Query allows checking to see if the long-running sequence is completed without waiting as with queryFinal.

        Args:
           id (str): runId of the sequence under execution

        Returns: SubmitResponse
      """
        response = self._postCommand(Query(id)._asDict())
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, response.text)
        return CommandResponse._fromDict(response.json())

    def queryFinal(self, runId: str, timeoutInSeconds: int) -> SubmitResponse:
        """
        Query for the final result of a long-running sequence which was sent through submit().

        Args:
           id (str): runId of the sequence under execution
           timeoutInSeconds (int): max-time in secs to wait for a final response

        Returns: SubmitResponse
            The final submit response
      """
        baseUri = self._getBaseUri().replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        respDict = QueryFinal(runId, timeoutInSeconds).to_dict()
        jsonStr = json.dumps(respDict)
        ws = create_connection(wsUri)
        ws.send(jsonStr)
        jsonResp = ws.recv()
        return CommandResponse._fromDict(json.loads(jsonResp))

    def submitAndWait(self, sequence: Sequence, timeoutInSeconds: int) -> SubmitResponse:
        """
        Submit the given sequence to the sequencer and wait for the final response if the sequence was successfully
        'Started'.
        If the sequencer is idle, the provided sequence will be submitted to the sequencer and the final response will
        be returned.
        If the sequencer is already running another sequence, an 'Invalid' response is returned.

        Args:
           sequence (Sequence): sequence to run on the sequencer
           timeoutInSeconds (int): max-time in secs to wait for a final response

        Returns: SubmitResponse
            The final submit response
      """
        resp = self.submit(sequence)
        match resp:
            case Started(runId):
                return self.queryFinal(runId, timeoutInSeconds)
            case _:
                return resp

    def goOnline(self) -> GoOnlineResponse:
        """
        sends command to the sequencer to go in Online state if it is in Offline state

        Returns: GoOnlineResponse
       """
        return self._postCommandGetResponse(GoOnline())

    def goOffline(self) -> GoOfflineResponse:
        """
        sends command to the sequencer to go in Offline state if it is in Online state

        Returns: GoOfflineResponse
       """
        return self._postCommandGetResponse(GoOffline())

    def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        """
        Sends command to the sequencer to call the diagnostic mode handler of the sequencer's script

        Args:
           startTime (UTCTime): time at which the diagnostic mode will take effect
           hint (str): String to support diagnostic data mode

        Returns: DiagnosticModeResponse
      """
        return self._postCommandGetResponse(DiagnosticMode(startTime, hint))

    def operationsMode(self) -> OperationsModeResponse:
        """
        Sends command to the sequencer to call the operations mode handler of the sequencer's script

        Returns: OperationsModeResponse
        """
        return self._postCommandGetResponse(OperationsMode())

    def getSequencerState(self) -> SequencerState:
        """
        Returns the current state of the sequencer (Idle, Loaded, Offline, Running, Processing)

        Returns: SequencerState
        """
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
