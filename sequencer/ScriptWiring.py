from dataclasses import dataclass

from sequencer.CswServices import CswServices
from sequencer.ScriptContext import ScriptContext


class ScriptWiring:

    def __init__(self, scriptContext: ScriptContext, cswServices: CswServices):
        self.scriptContext = scriptContext
        self.cswServices = cswServices

