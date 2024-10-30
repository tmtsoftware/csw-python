# /**
#  * Base Class for all the scripts(sequencer-script, FSM)
#  * which contains the implementation of handlers like onSetup, OnObserve, OnNewSequence etc.
#  *
#  * @constructor
#  *
#  * @param wiring - An instance of script wiring
#  */
from typing import Callable

from sequencer.CswHighLevelDsl import CswHighLevelDsl
from sequencer.ScriptDsl import ScriptDsl
from sequencer.ScriptScopes import HandlerScope
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
    def onNewSequence(self, func: Callable[[HandlerScope], None]):
        return self.scriptDsl.onNewSequence(func)

    def onGoOnline(self, func: Callable[[HandlerScope], None]):
        return self.scriptDsl.onGoOnline(func)

    def onGoOffline(self, func: Callable[[HandlerScope], None]):
        return self.scriptDsl.onGoOffline(func)

    def onAbortSequence(self, func: Callable[[HandlerScope], None]):
        return self.scriptDsl.onAbortSequence(func)

    def onShutdown(self, func: Callable[[HandlerScope], None]):
        return self.scriptDsl.onShutdown(func)

    def onDiagnosticMode(self, func: Callable[[HandlerScope, (UTCTime, str)], None]):
        return self.scriptDsl.onDiagnosticMode(func)

#     fun onDiagnosticMode(block: suspend HandlerScope.(UTCTime, String) -> Unit) =
#             scriptDsl.onDiagnosticMode { x: UTCTime, y: String ->
#                 coroutineScope.launch { block(this.toHandlerScope(), x, y) }.asCompletableFuture().thenAccept { }
#             }
#
#     fun onOperationsMode(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onOperationsMode { block.toCoroutineScope().toJava() }
#
#     fun onStop(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onStop { block.toCoroutineScope().toJava() }
#
#     internal fun CoroutineScope.toHandlerScope(): HandlerScope = object : HandlerScope by this@BaseScript {
#         override val coroutineContext: CoroutineContext = this@toHandlerScope.coroutineContext
#     }
#
#     private fun (suspend HandlerScope.() -> Unit).toCoroutineScope(): suspend (CoroutineScope) -> Unit =
#             { this(it.toHandlerScope()) }
# }
