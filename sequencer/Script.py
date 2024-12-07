from typing import Callable, Awaitable
from functools import wraps

from csw.ParameterSetType import Setup, Observe
from sequencer.BaseScript import BaseScript
from sequencer.CommandHandler import CommandHandler
from sequencer.ScriptError import ScriptError
from sequencer.ScriptWiring import ScriptWiring


class Script(BaseScript):
    def __init__(self, wiring: ScriptWiring):
        self.wiring = wiring
        BaseScript.__init__(self, wiring)

    def onSetup(self, name: str):
        def decorator(func: Callable[[Setup], Awaitable]):
            @wraps(func)
            def wrapper():
                # noinspection PyTypeChecker
                self.scriptDsl.onSetupCommand(name, CommandHandler(func))

            return wrapper

        return decorator

    def onObserve(self, name: str):
        def decorator(func: Callable[[Setup], Awaitable]):
            @wraps(func)
            def wrapper():
                # noinspection PyTypeChecker
                self.scriptDsl.onObserveCommand(name, CommandHandler(func))

            return wrapper

        return decorator

    def onGlobalError(self, func: Callable[[ScriptError], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onException(func)

        return wrapper
