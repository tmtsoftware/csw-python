from typing import Callable, Awaitable

from csw.ParameterSetType import Setup, Observe
from sequencer.BaseScript import BaseScript
from sequencer.CommandHandler import CommandHandler
from sequencer.ScriptError import ScriptError
from sequencer.ScriptWiring import ScriptWiring


class Script(BaseScript):
    def __init__(self, wiring: ScriptWiring):
        self.wiring = wiring
        BaseScript.__init__(self, wiring)

    def onSetup(self, name: str, func: Callable[[Setup], Awaitable]) -> CommandHandler:
        # noinspection PyTypeChecker
        handler = CommandHandler(func)
        self.scriptDsl.onSetupCommand(name, handler)
        return handler

    def onObserve(self, name: str, func: Callable[[Observe], Awaitable]) -> CommandHandler:
        # noinspection PyTypeChecker
        handler = CommandHandler(func)
        self.scriptDsl.onObserveCommand(name, handler)
        return handler

    def onGlobalError(self, func: Callable[[ScriptError], Awaitable]):
        self.scriptDsl.onException(func)
