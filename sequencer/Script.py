from typing import Callable, Awaitable
from functools import wraps

from csw.ParameterSetType import Setup, Observe
from sequencer.BaseScript import BaseScript
from sequencer.CommandHandler import CommandHandler
from sequencer.ScriptError import ScriptError
from sequencer.ScriptWiring import ScriptWiring

# ----- decorators -------
def onSetup(name: str):
    def decorator(func: Callable[[Setup], Awaitable]):
        @wraps(func)
        def wrapper(self):
            return self.onSetup(name, func)
        return wrapper
    return decorator

def onObserve(name: str):
    def decorator(func: Callable[[Setup], Awaitable]):
        @wraps(func)
        def wrapper(self):
            return self.onObserve(name, func)
        return wrapper
    return decorator

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
