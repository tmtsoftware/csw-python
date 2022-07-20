import pytest

from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from esw.SequencerClient import SequencerClient


# Note: Before running this test, start the esw-observing-simulation and load the sequence
# "esw_imager_only_sequence.json".

# @pytest.mark.skip(reason="Requires running ESW observing simulation from the esw-observing-simulation repo")
class TestSequencerClient:
    seqClient = SequencerClient(Prefix(Subsystems.ESW, "IRIS_ImagerOnly"))

    def test_get_sequence(self):
        stepList = self.seqClient.getSequence()
        print(f'\nSequence has {len(stepList.steps)} steps')
        assert(len(stepList.steps) == 11)
        print(f'First step is {stepList.steps[0]}')
        assert(stepList.steps[0].command.commandName.name == "observationStart")
