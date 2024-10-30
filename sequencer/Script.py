from typing import Callable

from csw.ParameterSetType import Setup, Observe, SequenceCommand
from sequencer.BaseScript import BaseScript
from sequencer.CommandHandler import CommandHandler
from sequencer.ScriptError import ScriptError
from sequencer.ScriptWiring import ScriptWiring


class Script(BaseScript):
    def __init__(self, wiring: ScriptWiring):
        self.wiring = wiring
        BaseScript.__init__(self, wiring)

    def onSetup(self, name: str, func: Callable[[Setup], None]) -> CommandHandler:
        # noinspection PyTypeChecker
        handler = CommandHandler(self, func)
        self.scriptDsl.onSetupCommand(name, handler)
        return handler

    def onObserve(self, name: str, func: Callable[[Observe], None]) -> CommandHandler:
        # noinspection PyTypeChecker
        handler = CommandHandler(self, func)
        self.scriptDsl.onObserveCommand(name, handler)
        return handler

    def onGlobalError(self, func: Callable[[ScriptError], None]):
        self.scriptDsl.onException(func)
