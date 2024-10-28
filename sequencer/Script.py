from sequencer.BaseScript import BaseScript
from sequencer.ScriptScopes import CommandHandlerScope, ScriptScope
from sequencer.ScriptWiring import ScriptWiring


class Script(BaseScript, ScriptScope):
    def __init__(self, wiring: ScriptWiring):
        self.wiring = wiring
        BaseScript.__init__(self, wiring)


def script():
    pass