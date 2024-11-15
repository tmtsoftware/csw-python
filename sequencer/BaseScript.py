# /**
#  * Base Class for all the scripts(sequencer-script, FSM)
#  * which contains the implementation of handlers like onSetup, OnObserve, OnNewSequence etc.
#  *
#  * @constructor
#  *
#  * @param wiring - An instance of script wiring
#  */
from typing import Callable

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
        CswHighLevelDsl.__init__(self, wiring.cswServices, wiring.scriptContext)
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
    def onNewSequence(self, func: Callable):
        return self.scriptDsl.onNewSequence(func)

    def onGoOnline(self, func: Callable):
        return self.scriptDsl.onGoOnline(func)

    def onGoOffline(self, func: Callable):
        return self.scriptDsl.onGoOffline(func)

    def onAbortSequence(self, func: Callable):
        return self.scriptDsl.onAbortSequence(func)

    def onShutdown(self, func: Callable):
        return self.scriptDsl.onShutdown(func)

    def onDiagnosticMode(self, func: Callable[[UTCTime, str], None]):
        return self.scriptDsl.onDiagnosticMode(func)

    def onOperationsMode(self, func: Callable):
        return self.scriptDsl.onOperationsMode(func)

    def onStop(self, func: Callable):
        return self.scriptDsl.onStop(func)

