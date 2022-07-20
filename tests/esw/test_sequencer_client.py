import pytest

from csw.Parameter import IntKey
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from esw.SequencerClient import SequencerClient

# Note: Before running this test, start the esw-observing-simulation and load the sequence
# "esw_imager_only_sequence.json".

# @pytest.mark.skip(reason="Requires running ESW observing simulation from the esw-observing-simulation repo")
from esw.SequencerRes import Ok, Unhandled


class TestSequencerClient:
    seqClient = SequencerClient(Prefix(Subsystems.ESW, "IRIS_ImagerOnly"))
    prefix = Prefix(Subsystems.CSW, "TestClient")
    maybeObsId = []
    param = IntKey.make("testValue").set(42)
    paramSet = [param]

    def _makeSetup(self, name: str):
        return Setup(self.prefix, CommandName(name), self.maybeObsId, self.paramSet)

    def test_get_sequence(self):
        stepList = self.seqClient.getSequence()
        if (stepList != None):
            print(f'\nSequence has {len(stepList.steps)} steps')
            # assert (len(stepList.steps) == 11)
            print(f'First step is {stepList.steps[0]}')
            # assert (stepList.steps[0].command.commandName.name == "observationStart")
        else:
            print("StepList is empty")
            pytest.fail("Expected stepList to contain a sequence")

    def test_is_available(self):
        assert (self.seqClient.isAvailable() == False)

    def test_is_online(self):
        assert (self.seqClient.isOnline() == True)

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

    def test_insert_after(self):
        stepList = self.seqClient.getSequence()
        id = stepList.steps[0].id
        setup = self._makeSetup("TestInsertAfter")
        resp = self.seqClient.insertAfter(id, [setup])
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
