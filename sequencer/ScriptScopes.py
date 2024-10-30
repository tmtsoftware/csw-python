from typing import Callable

from csw.ParameterSetType import Setup, Observe
from csw.UTCTime import UTCTime
from sequencer.CommandHandler import CommandHandler
from sequencer.CswHighLevelDsl import CswHighLevelDslApi
from sequencer.ScriptError import ScriptError

# TODO: add BecomeDsl
HandlerScope = CswHighLevelDslApi

# TODO:add NextIfDsl
CommandHandlerScope = HandlerScope


class CommonHandlers:
    def onGoOnline(func: Callable[[HandlerScope], None]):
        pass

    def onGoOffline(func: Callable[[HandlerScope], None]):
        pass

    def onAbortSequence(func: Callable[[HandlerScope], None]):
        pass

    def onShutdown(func: Callable[[HandlerScope], None]):
        pass

    def onDiagnosticMode(func: Callable[[HandlerScope, UTCTime, str], None]):
        pass

    def onOperationsMode(func: Callable[[HandlerScope], None]):
        pass

    def onStop(func: Callable[[HandlerScope], None]):
        pass

    def onNewSequence(func: Callable[[HandlerScope], None]):
        pass


class ScriptHandlers:
    def onSetup(self, name: str, func: Callable[[CommandHandlerScope, Setup], None]) -> CommandHandler:
        pass

    def onObserve(self, name: str, func: Callable[[CommandHandlerScope, Observe], None]) -> CommandHandler:
        pass

    def onGlobalError(self, func:  Callable[[HandlerScope, ScriptError], None]):
        pass

# XXX TODO
    # def loadScripts(vararg reusableScriptResult: ReusableScriptResult)


class ScriptScope(ScriptHandlers, CommonHandlers):
        pass
