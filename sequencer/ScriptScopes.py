from typing import Callable

from csw.ParameterSetType import Setup, Observe
from sequencer.CommandHandler import CommandHandler
from sequencer.CswHighLevelDslApi import CswHighLevelDslApi

class HandlerScope(CswHighLevelDslApi):
    pass

class CommandHandlerScope(HandlerScope, NextIfDsl):

# func: Callable[[], None]
class CommonHandlers(CswHighLevelDslApi):
    def onGoOnline(block: suspend HandlerScope.() -> Unit)
    def onGoOffline(block: suspend HandlerScope.() -> Unit)
    def onAbortSequence(block: suspend HandlerScope.() -> Unit)
    def onShutdown(block: suspend HandlerScope.() -> Unit)
    def onDiagnosticMode(block: suspend HandlerScope.(UTCTime, String) -> Unit)
    def onOperationsMode(block: suspend HandlerScope.() -> Unit)
    def onStop(block: suspend HandlerScope.() -> Unit)
    def onNewSequence(block: suspend HandlerScope.() -> Unit)

class ScriptHandlers():
    def onSetup(self, name: str, func: Callable[[Setup], None]) -> CommandHandler:
        pass

    def onObserve(self, name: str, func: Callable[[Observe], None]) -> CommandHandler:
        pass

    # XXX TODO
    # def onGlobalError(block: suspend HandlerScope.(ScriptError) -> Unit)
    # def loadScripts(vararg reusableScriptResult: ReusableScriptResult)


class ScriptScope(ScriptHandlers, CommonHandlers):
    pass
