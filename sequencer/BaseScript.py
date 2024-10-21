# /**
#  * Base Class for all the scripts(sequencer-script, FSM)
#  * which contains the implementation of handlers like onSetup, OnObserve, OnNewSequence etc.
#  *
#  * @constructor
#  *
#  * @param wiring - An instance of script wiring
#  */
from csw.SequencerObserveEvent import SequencerObserveEvent
from esw.ObsMode import ObsMode
from sequencer.CswHighLevelDslApi import CswHighLevelDslApi, CswHighLevelDsl
from sequencer.CswServices import CswServices
from sequencer.ScriptContext import ScriptContext
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
        CswHighLevelDsl.__init__(self, wiring.cswServices, wiring.scriptContext)
        self.scriptDsl = ScriptDsl(
            wiring.scriptContext.sequenceOperatorFactory(),
            logger,
            strandEc,
            shutdownTask
        )

    # self.isOnline: bool =
        self.prefix: str = str(self.wiring.scriptContext.prefix)
        self.obsMode: ObsMode = self.wiring.scriptContext.obsMode
        self.sequencerObserveEvent: SequencerObserveEvent = SequencerObserveEvent(self.wiring.scriptContext.prefix)


# (CswHighLevelDsl(wiring.cswServices, wiring.scriptContext), HandlerScope):
    # (wiring: ScriptWiring) :
#     override val actorSystem: ActorSystem<SpawnProtocol.Command> = wiring.scriptContext.actorSystem()
#     protected val shutdownTask = Runnable { wiring.shutdown() }
#     internal open val scriptDsl: ScriptDsl by lazy {
#         ScriptDsl(
#                 wiring.scriptContext.sequenceOperatorFactory(),
#                 logger,
#                 strandEc,
#                 shutdownTask
#         )
#     }
#     override val isOnline: Boolean get() = scriptDsl.isOnline
#     final override val prefix: String = wiring.scriptContext.prefix().toString()
#     final override val obsMode: ObsMode = wiring.scriptContext.obsMode()
#     override val sequencerObserveEvent: SequencerObserveEvent = SequencerObserveEvent(Prefix.apply(prefix))
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
#     override val coroutineScope: CoroutineScope = wiring.scope + exceptionHandler
#
#     private val shutdownHandlerCoroutineScope = wiring.scope + shutdownExceptionHandler
#
#     fun onNewSequence(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onNewSequence { block.toCoroutineScope().toJava() }
#
#     fun onGoOnline(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onGoOnline { block.toCoroutineScope().toJava() }
#
#     fun onGoOffline(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onGoOffline { block.toCoroutineScope().toJava() }
#
#     fun onAbortSequence(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onAbortSequence { block.toCoroutineScope().toJava() }
#
#     fun onShutdown(block: suspend HandlerScope.() -> Unit) =
#             scriptDsl.onShutdown {
#                 block.toCoroutineScope().toJava(shutdownHandlerCoroutineScope).whenComplete { _, _ ->
#                     // cleanup cpu bound dispatcher in case script has used it, as a part of shutdown process
#                     shutdownCpuBoundDispatcher()
#                 }
#             }
#
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
