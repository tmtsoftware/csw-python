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
        self.setupCommandHandler ++ that.setupCommandHandler
        self.observerCommandHandler ++ that.observerCommandHandler
        self.onlineHandlers ++ that.onlineHandlers
        self.offlineHandlers ++ that.offlineHandlers
        self.shutdownHandlers ++ that.shutdownHandlers
        self.abortHandlers ++ that.abortHandlers
        self.stopHandlers ++ that.stopHandlers
        self.diagnosticHandlers ++ that.diagnosticHandlers
        self.operationsHandlers ++ that.operationsHandlers
        self.exceptionHandlers ++ that.exceptionHandlers
        return self
