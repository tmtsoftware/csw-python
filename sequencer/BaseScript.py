# /**
#  * Base Class for all the scripts(sequencer-script, FSM)
#  * which contains the implementation of handlers like onSetup, OnObserve, OnNewSequence etc.
#  *
#  * @constructor
#  *
#  * @param wiring - An instance of script wiring
#  */
from functools import wraps
from typing import Callable, Awaitable

from csw.UTCTime import UTCTime
from sequencer.CswHighLevelDsl import CswHighLevelDsl
from sequencer.ScriptDsl import ScriptDsl
from sequencer.ScriptWiring import ScriptWiring


class BaseScript(CswHighLevelDsl):
    """
    Base Class for all the scripts(sequencer-script, FSM)
    which contains the implementation of handlers like onSetup, OnObserve, OnNewSequence etc.
    """

    def __init__(self, wiring: ScriptWiring):
        self.wiring = wiring
        # self.shutdownTask = wiring.shutdown
        CswHighLevelDsl.__init__(self, cswServices = wiring.cswServices, scriptContext = wiring.scriptContext)
        self.scriptDsl = ScriptDsl(wiring.scriptContext.sequenceOperatorFactory)

#
#     private val exceptionHandler = CoroutineExceptionHandler { _, exception ->
#         error("Exception thrown in script with the message: [${exception.message}], invoking exception handler")
#         scriptDsl.executeExceptionHandlers(exception)
#     }
#
#     private val shutdownExceptionHandler = CoroutineExceptionHandler { _, exception ->
#         error("Shutting down: Exception thrown in script with the message: [${exception.message}]")
#     }
#

    def onNewSequence(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onNewSequence(func)
        return wrapper

    def onGoOnline(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onGoOnline(func)
        return wrapper

    def onGoOffline(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onGoOffline(func)
        return wrapper

    def onAbortSequence(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onAbortSequence(func)
        return wrapper

    def onShutdown(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onShutdown(func)
        return wrapper

    def onDiagnosticMode(self):
        def wrapper(func: Callable[[UTCTime, str], Awaitable]):
            self.scriptDsl.onDiagnosticMode(func)
        return wrapper

    def onOperationsMode(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onOperationsMode(func)
        return wrapper

    def onStop(self):
        def wrapper(func: Callable[[], Awaitable]):
            self.scriptDsl.onStop(func)
        return wrapper


