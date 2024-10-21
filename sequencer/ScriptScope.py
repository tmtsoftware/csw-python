from typing import Callable

from csw.ParameterSetType import Setup, Observe
from sequencer.CommandHandler import CommandHandler
from sequencer.CswHighLevelDslApi import CswHighLevelDslApi
from sequencer.ScriptError import ScriptError
from sequencer.ScriptScopes import HandlerScope


class CommonHandlers(CswHighLevelDslApi):
    def onGoOnline(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onGoOffline(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onAbortSequence(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onShutdown(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onDiagnosticMode(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onOperationsMode(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onStop(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass

    def onNewSequence(func:  Callable[[HandlerScope], None]) -> CommandHandler:
        pass


class ScriptHandlers:
    def onSetup(name: str, func:  Callable[[CommandHandlerScope, Setup], None]) -> CommandHandler:
        pass

    def onObserve(name: str, func:  Callable[[CommandHandlerScope, Observe], None]) -> CommandHandler:
        pass

    def onGlobalError(func:  Callable[[HandlerScope, ScriptError], None]) -> CommandHandler:
        pass

    # def loadScripts(reusableScriptResult: ReusableScriptResult)
