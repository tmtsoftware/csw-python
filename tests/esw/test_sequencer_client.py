import pytest

from csw.CommandResponse import Started, Error
from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from csw.UTCTime import UTCTime
from esw.Sequence import Sequence
from esw.SequencerClient import SequencerClient
from esw.EswSequencerResponse import Ok, Unhandled, SequencerState

# Note: Before running this test, start the esw-observing-simulation and load the sequence
# "esw_imager_only_sequence.json".


# noinspection PyShadowingBuiltins
@pytest.mark.skip(reason="Requires running ESW observing simulation from the esw-observing-simulation repo")
class TestSequencerClient:
    sequencerPrefix = Prefix(Subsystem.ESW, "IRIS_ImagerOnly")
    seqClient = SequencerClient(sequencerPrefix)
    clientPrefix = Prefix(Subsystem.CSW, "TestClient")
    maybeObsId = []
    param = IntKey.make("testValue").set(42)
    paramSet = [param]

    def _makeSetup(self, name: str):
        return Setup(self.clientPrefix, CommandName(name), self.maybeObsId, self.paramSet)

    def test_get_sequence(self):
        stepList = self.seqClient.getSequence()
        if stepList is not None:
            print(f'\nSequence has {len(stepList.steps)} steps')
            print(f'First step is {stepList.steps[0]}')
        else:
            print("StepList is empty")
            pytest.fail("Expected stepList to contain a sequence")

    def test_is_available(self):
        assert (self.seqClient.isAvailable() is False)

    def test_is_online(self):
        assert (self.seqClient.isOnline() is True)

    def test_add(self):
        setup = self._makeSetup("Test")
        resp = self.seqClient.add([setup])
        assert (isinstance(resp, Ok))

    def test_prepend(self):
        setup = self._makeSetup("Test")
        resp = self.seqClient.prepend([setup])
        assert (isinstance(resp, Ok))

    def test_replace(self):
        stepList = self.seqClient.getSequence()
        id = stepList.steps[0].id
        setup = self._makeSetup("TestReplace")
        resp = self.seqClient.replace(id, [setup])
        assert (isinstance(resp, Ok))

    def test_delete(self):
        stepList = self.seqClient.getSequence()
        id = stepList.steps[0].id
        resp = self.seqClient.delete(id)
        assert (isinstance(resp, Ok))

    def test_pause(self):
        resp = self.seqClient.pause()
        assert (isinstance(resp, Unhandled))

    def test_resume(self):
        resp = self.seqClient.resume()
        assert (isinstance(resp, Unhandled))

    def test_add_breakpoint(self):
        stepList = self.seqClient.getSequence()
        id = stepList.steps[0].id
        resp = self.seqClient.addBreakpoint(id)
        assert (isinstance(resp, Ok))

    # def test_start_sequence(self):
    #     resp = self.seqClient.startSequence()
    #     assert (isinstance(resp, Ok))

    def test_remove_breakpoint(self):
        stepList = self.seqClient.getSequence()
        id = stepList.steps[0].id
        resp = self.seqClient.removeBreakpoint(id)
        assert (isinstance(resp, Ok))

    def test_reset(self):
        resp = self.seqClient.reset()
        assert (isinstance(resp, Ok))

    def test_abort_sequence(self):
        resp = self.seqClient.abortSequence()
        assert (isinstance(resp, Unhandled))

    def test_stop(self):
        resp = self.seqClient.stop()
        assert (isinstance(resp, Unhandled))

    def test_load_sequence(self):
        setup1 = self._makeSetup("Test1")
        setup2 = self._makeSetup("Test2")
        setup3 = self._makeSetup("Test3")
        sequence = Sequence([setup1, setup2, setup3])
        resp = self.seqClient.loadSequence(sequence)
        assert (isinstance(resp, Ok))

    def test_submit(self):
        setup = self._makeSetup("Test")
        resp = self.seqClient.submit(Sequence([setup]))
        assert (isinstance(resp, Started))

    def test_query(self):
        setup = self._makeSetup("Test")
        resp1 = self.seqClient.submit(Sequence([setup]))
        resp2 = self.seqClient.query(resp1.runId)
        assert (isinstance(resp1, Started))
        assert (isinstance(resp2, Error))

    def test_query_final(self):
        setup = self._makeSetup("Test")
        resp1 = self.seqClient.submit(Sequence([setup]))
        resp2 = self.seqClient.queryFinal(resp1.runId, 2)
        assert (isinstance(resp1, Started))
        assert (isinstance(resp2, Error))

    def test_submit_and_wait(self):
        setup = self._makeSetup("Test")
        resp = self.seqClient.submitAndWait(Sequence([setup]), 2)
        assert (isinstance(resp, Error))

    def test_go_offline(self):
        resp = self.seqClient.goOffline()
        assert (isinstance(resp, Ok))

    def test_go_online(self):
        resp = self.seqClient.goOnline()
        assert (isinstance(resp, Ok))

    def test_diagnostic_mode(self):
        resp = self.seqClient.diagnosticMode(UTCTime.now(), "some hint")
        assert (isinstance(resp, Ok))

    def test_operations_mode(self):
        resp = self.seqClient.operationsMode()
        assert (isinstance(resp, Ok))

    def test_get_sequencer_state(self):
        resp = self.seqClient.getSequencerState()
        assert (resp == SequencerState.Idle)
