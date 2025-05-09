import json
import uuid
from datetime import timedelta

from aiohttp import ClientResponse, ClientSession

from csw.CommandResponse import SubmitResponse, CommandResponse, Started, Error
from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from esw.Sequence import Sequence
from esw.SequencerRequest import *
from esw.EswSequencerResponse import *
from esw.StepList import StepList

# noinspection PyProtectedMember,PyShadowingBuiltins
from esw.WsCommands import QueryFinal
from sequencer.SequencerApi import SequencerApi


# noinspection DuplicatedCode,PyShadowingBuiltins
class SequencerClient(SequencerApi):

    def __init__(self, prefix: Prefix, clientSession: ClientSession):
        self.prefix = prefix
        self._session = clientSession

    async def post(self, url: str, headers: dict, jsonData: str) -> ClientResponse:
        return await self._session.post(url, headers=headers, json=jsonData)

    async def _getBaseUri(self) -> str:
        locationService = LocationService(self._session)
        connection = ConnectionInfo.make(self.prefix, ComponentType.Sequencer, ConnectionType.HttpType)
        location = await locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    async def _postCommand(self, data: dict) -> ClientResponse:
        baseUri = await self._getBaseUri()
        postUri = f"{baseUri}post-endpoint"
        headers = {'Content-type': 'application/json'}
        jsonData = json.loads(json.dumps(data))
        return await self.post(postUri, headers=headers, jsonData=jsonData)

    async def _postCommandGetResponse(self, request: SequencerRequest) -> EswSequencerResponse:
        response = await self._postCommand(request._asDict())
        if not response.ok:
            return Unhandled("Unknown", request.__class__.__name__, f"Error: {await response.text()}")
        return EswSequencerResponse._fromDict(await response.json())

    async def getSequence(self) -> StepList | None:
        """
        Get the sequence in sequencer - current or last.
        If there is no sequence
        then None response is returned
        otherwise a StepList is returned.

        Returns: StepList
            a list of steps in the sequence
       """
        response = await self._postCommand(GetSequence()._asDict())
        if not response.ok:
            return None
        return StepList._fromDict(await response.json())

    async def isAvailable(self) -> bool:
        """
        Checks if sequencer is in Idle state.

        Returns: bool
            true if the sequencer is available
       """
        response = await self._postCommand(IsAvailable()._asDict())
        if not response.ok:
            return False
        return await response.json()

    async def isOnline(self) -> bool:
        """
        Checks if sequencer is in Online(any state except Offline) state

        Returns: bool
            true if the sequencer is online
       """
        response = await self._postCommand(IsOnline()._asDict())
        if not response.ok:
            return False
        return await response.json()

    async def add(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        """
        Adds the given list of sequence commands at the end of the sequence

        Args:
            commands (List[SequenceCommand]): list of SequenceCommand to add in the sequence of sequencer

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(Add(commands))

    async def prepend(self, commands: List[SequenceCommand]) -> OkOrUnhandledResponse:
        """
        Prepends the given list of sequence commands in the sequence

        Args:
            commands (List[SequenceCommand]): list of SequenceCommand to prepend in the sequence of sequencer

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(Prepend(commands))

    async def replace(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        """
        Replaces the command of the given id with the given list of sequence commands in the sequence

        Args:
            id (str): runId of command which is to be replaced
            commands (List[SequenceCommand]): list of SequenceCommand to replace with

        Returns: GenericResponse
       """
        return await self._postCommandGetResponse(Replace(id, commands))

    async def insertAfter(self, id: str, commands: List[SequenceCommand]) -> GenericResponse:
        """
        Inserts the given list of sequence commands after the command of given id in the sequence

        Args:
            id (str): runId of command after which the given list of commands is to be inserted
            commands (List[SequenceCommand]): list of SequenceCommand to be inserted

        Returns: GenericResponse
       """
        return await self._postCommandGetResponse(InsertAfter(id, commands))

    async def delete(self, id: str) -> GenericResponse:
        """
        Deletes the command of the given id in the sequence

        Args:
            id (str): runId of the command which is to be deleted

        Returns: GenericResponse
       """
        return await self._postCommandGetResponse(Delete(id))

    async def pause(self) -> PauseResponse:
        """
        Pauses the running sequence

        Returns: PauseResponse
       """
        return await self._postCommandGetResponse(Pause())

    async def resume(self) -> OkOrUnhandledResponse:
        """
        Resumes the paused sequence

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(Resume())

    async def addBreakpoint(self, id: str) -> GenericResponse:
        """
        Adds a breakpoint at the command of the given id in the sequence

        Args:
            id (str): runId of the command where breakpoint is to be added

        Returns: GenericResponse
       """
        return await self._postCommandGetResponse(AddBreakpoint(id))

    async def removeBreakpoint(self, id: str) -> GenericResponse:
        """
       Removes a breakpoint from the command of the given id in the sequence

       Args:
           id (str): runId of command where breakpoint is set

       Returns: GenericResponse
      """
        return await self._postCommandGetResponse(RemoveBreakpoint(id))

    async def reset(self) -> OkOrUnhandledResponse:
        """
        Resets the sequence by discarding all the pending steps of the sequence

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(Reset())

    async def abortSequence(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the abort handler of the sequencer's script

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(AbortSequence())

    async def stop(self) -> OkOrUnhandledResponse:
        """
        Discards all the pending steps of the sequence and call the stop handler of the sequencer's script

        Returns: OkOrUnhandledResponse
       """
        return await self._postCommandGetResponse(Stop())

    # --- commandApi ---

    async def loadSequence(self, sequence: Sequence) -> OkOrUnhandledResponse:
        """
        Loads the given sequence to the sequencer.
        If the sequencer is in Idle or Loaded state
        then Ok response is returned
        otherwise Unhandled response is returned

        Args:
           sequence (Sequence): sequence to run on the sequencer

        Returns: OkOrUnhandledResponse
      """
        return await self._postCommandGetResponse(LoadSequence(sequence.commands))

    async def startSequence(self) -> SubmitResponse:
        """
        Starts the loaded sequence in the sequencer.
        If the sequencer is loaded then a Started response is returned.
        If the sequencer is already running another sequence, an Invalid response is returned.

        Returns: SubmitResponse
            an initial SubmitResponse
       """
        return await self._postCommandGetResponse(StartSequence())

    async def submit(self, sequence: Sequence) -> SubmitResponse:
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
        response = await self._postCommand(Submit(sequence.commands)._asDict())
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, await response.text())
        return CommandResponse._fromDict(await response.json())

    async def query(self, id: str) -> SubmitResponse:
        """
        Query for the result of the sequence which was submitted to get a SubmitResponse.
        Query allows checking to see if the long-running sequence is completed without waiting as with queryFinal.

        Args:
           id (str): runId of the sequence under execution

        Returns: SubmitResponse
      """
        response = await self._postCommand(Query(id)._asDict())
        if not response.ok:
            runId = str(uuid.uuid4())
            return Error(runId, await response.text())
        return CommandResponse._fromDict(await response.json())

    async def queryFinal(self, runId: str, timeout: timedelta = timedelta(seconds=10)) -> SubmitResponse:
        """
        Query for the final result of a long-running sequence which was sent through submit().

        Args:
           runId (str): runId of the sequence under execution
           timeout (timedelta): max-time in secs to wait for a final response

        Returns: SubmitResponse
            The final submit response
      """
        baseUri = (await self._getBaseUri()).replace('http:', 'ws:')
        wsUri = f"{baseUri}websocket-endpoint"
        # noinspection PyUnresolvedReferences
        respDict = QueryFinal(runId, int(timeout.total_seconds())).to_dict()
        jsonStr = json.dumps(respDict)
        ws = await self._session.ws_connect(wsUri)
        await ws.send_str(jsonStr)
        jsonResp = await ws.receive_str()
        await ws.close()
        return CommandResponse._fromDict(json.loads(jsonResp))

    async def submitAndWait(self, sequence: Sequence, timeout: timedelta) -> SubmitResponse:
        """
        Submit the given sequence to the sequencer and wait for the final response if the sequence was successfully
        'Started'.
        If the sequencer is idle, the provided sequence will be submitted to the sequencer and the final response will
        be returned.
        If the sequencer is already running another sequence, an 'Invalid' response is returned.

        Args:
           sequence (Sequence): sequence to run on the sequencer
           timeout (timedelta): max-time in secs to wait for a final response

        Returns: SubmitResponse
            The final submit response
      """
        resp = await self.submit(sequence)
        match resp:
            case Started(runId):
                return await self.queryFinal(runId, timeout)
            case _:
                return resp

    async def goOnline(self) -> GoOnlineResponse:
        """
        sends command to the sequencer to go in Online state if it is in Offline state

        Returns: GoOnlineResponse
       """
        return await self._postCommandGetResponse(GoOnline())

    async def goOffline(self) -> GoOfflineResponse:
        """
        sends command to the sequencer to go in Offline state if it is in Online state

        Returns: GoOfflineResponse
       """
        return await self._postCommandGetResponse(GoOffline())

    async def diagnosticMode(self, startTime: UTCTime, hint: str) -> DiagnosticModeResponse:
        """
        Sends command to the sequencer to call the diagnostic mode handler of the sequencer's script

        Args:
           startTime (UTCTime): time at which the diagnostic mode will take effect
           hint (str): String to support diagnostic data mode

        Returns: DiagnosticModeResponse
      """
        return await self._postCommandGetResponse(DiagnosticMode(startTime, hint))

    async def operationsMode(self) -> OperationsModeResponse:
        """
        Sends command to the sequencer to call the operations mode handler of the sequencer's script

        Returns: OperationsModeResponse
        """
        return await self._postCommandGetResponse(OperationsMode())

    async def getSequencerState(self) -> SequencerState:
        """
        Returns the current state of the sequencer (Idle, Loaded, Offline, Running, Processing)

        Returns: SequencerState
        """
        response = await self._postCommand(GetSequencerState()._asDict())
        if not response.ok:
            return SequencerState.Offline
        jsonData = await response.json()
        match jsonData["_type"]:
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

    # --- For script use ---

    async def pullNext(self) -> PullNextResponse:
        return await self._postCommandGetResponse(PullNext())

    async def maybeNext(self) -> MaybeNextResponse:
        return await self._postCommandGetResponse(MaybeNext())

    async def readyToExecuteNext(self) -> OkOrUnhandledResponse:
        return await self._postCommandGetResponse(ReadyToExecuteNext())

    async def stepSuccess(self):
        await self._postCommandGetResponse(StepSuccess())

    async def stepFailure(self, message: str):
        await self._postCommandGetResponse(StepFailure(message))
