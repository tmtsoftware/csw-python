from csw.ParameterSetType import Setup, Observe
from csw.UTCTime import UTCTime
from sequencer.FunctionBuilder import FunctionBuilder
from sequencer.FunctionHandlers import FunctionHandlers
from sequencer.ScriptApi import ScriptApi
from typing import Self


class ScriptDsl(ScriptApi):
    isOnline = True
    setupCommandHandler = FunctionBuilder[str, Setup, None]()
    observerCommandHandler = FunctionBuilder[str, Observe, None]()

    onlineHandlers = FunctionHandlers[None, None]()                      
    offlineHandlers = FunctionHandlers[None, None]()                     
    shutdownHandlers = FunctionHandlers[None, None]()                    
    abortHandlers = FunctionHandlers[None, None]()                       
    stopHandlers = FunctionHandlers[None, None]()                        
    diagnosticHandlers = FunctionHandlers[(UTCTime, str), None]()
    operationsHandlers = FunctionHandlers[None, None]()                  
    exceptionHandlers = FunctionHandlers[Exception, None]()
    newSequenceHandlers = FunctionHandlers[None, None]()

    @classmethod
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
