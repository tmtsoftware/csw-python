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
    def onNewSequence(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onNewSequence(func)
        return wrapper

    def onGoOnline(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onGoOnline(func)
        return wrapper

    def onGoOffline(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onGoOffline(func)
        return wrapper

    def onAbortSequence(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onAbortSequence(func)
        return wrapper

    def onShutdown(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onShutdown(func)
        return wrapper

    def onDiagnosticMode(self, func: Callable[[UTCTime, str], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onDiagnosticMode(func)
        return wrapper

    def onOperationsMode(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onOperationsMode(func)
        return wrapper

    def onStop(self, func: Callable[[], Awaitable]):
        @wraps(func)
        def wrapper():
            self.scriptDsl.onStop(func)
        return wrapper


