from csw.ParameterSetType import Setup, Observe
from csw.UTCTime import UTCTime
from sequencer.FunctionBuilder import FunctionBuilder
from sequencer.FunctionHandlers import FunctionHandlers
from sequencer.ScriptApi import ScriptApi
from typing import Self, Callable

from sequencer.SequenceOperatorApi import SequenceOperatorHttp


class ScriptDsl(ScriptApi):

    def __init__(self, sequenceOperatorFactory: Callable[[], SequenceOperatorHttp]):
        self.sequenceOperatorFactory = sequenceOperatorFactory
        self.isOnline = True
        self.setupCommandHandler = FunctionBuilder[str, Setup, None]()
        self.observerCommandHandler = FunctionBuilder[str, Observe, None]()

        self.onlineHandlers = FunctionHandlers[None, None]()
        self.offlineHandlers = FunctionHandlers[None, None]()
        self.shutdownHandlers = FunctionHandlers[None, None]()
        self.abortHandlers = FunctionHandlers[None, None]()
        self.stopHandlers = FunctionHandlers[None, None]()
        self.diagnosticHandlers = FunctionHandlers[(UTCTime, str), None]()
        self.operationsHandlers = FunctionHandlers[None, None]()
        self.exceptionHandlers = FunctionHandlers[Exception, None]()
        self.newSequenceHandlers = FunctionHandlers[None, None]()


    def merge(self, that: Self) -> Self:
        self.setupCommandHandler.merge(that.setupCommandHandler)
        self.observerCommandHandler.merge(that.observerCommandHandler)
        self.onlineHandlers.merge(that.onlineHandlers)
        self.offlineHandlers.merge(that.offlineHandlers)
        self.shutdownHandlers.merge(that.shutdownHandlers)
        self.abortHandlers.merge(that.abortHandlers)
        self.stopHandlers.merge(that.stopHandlers)
        self.diagnosticHandlers.merge(that.diagnosticHandlers)
        self.operationsHandlers.merge(that.operationsHandlers)
        self.exceptionHandlers.merge(that.exceptionHandlers)
        return self
