import sys
import os
import json

import structlog
from _pytest import pathlib

from esw.SequencerRequest import LoadSequence

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestEswContract:
    log = structlog.get_logger()

    # Validate against Command Service model contract file produced by csw
    def test_sequencer_service_models(self):
        testDir = pathlib.Path(__file__).parent.absolute()
        with open(f"{testDir}/http-contract.json") as json_file:
            data = json.load(json_file)
            requests = data['requests']
            #
            loadSequence: LoadSequence = LoadSequence._fromDict(requests['LoadSequence'][0])
            setup = loadSequence.sequence[0]
            assert setup.__class__.__name__ == 'Setup'
            assert setup.commandName.name == 'move'
            observe = loadSequence.sequence[1]
            assert observe.__class__.__name__ == 'Observe'
            assert observe.commandName.name == 'move'
            wait = loadSequence.sequence[2]
            assert wait.__class__.__name__ == 'Wait'
            assert wait.commandName.name == 'move'
            #
