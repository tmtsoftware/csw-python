from dataclasses import dataclass

from sequencer.CswServices import CswServices
from sequencer.ScriptContext import ScriptContext


class ScriptWiring:

    def __init__(self, scriptContext: ScriptContext):
        self.scriptContext = scriptContext
        self.cswServices: CswServices = CswServices.create(scriptContext)

