from csw.ParameterSetType import Setup, Observe, SequenceCommand
from csw.UTCTime import UTCTime
from esw.EswSequencerResponse import PullNextResult, Unhandled
from esw.Step import Step
from sequencer.CommandHandler import CommandHandler
from sequencer.FunctionBuilder import FunctionBuilder
from sequencer.FunctionHandlers import FunctionHandlers
from sequencer.ScriptApi import ScriptApi
from typing import Self, Callable

from sequencer.ScriptScopes import HandlerScope
from sequencer.SequenceOperatorApi import SequenceOperatorHttp


class ScriptDsl(ScriptApi):

    def __init__(self, sequenceOperatorFactory: Callable[[], SequenceOperatorHttp]):
        self.sequenceOperatorFactory = sequenceOperatorFactory
        self.isOnline = True
        self.setupCommandHandler = FunctionBuilder[str, Setup, None]()
        self.observerCommandHandler = FunctionBuilder[str, Observe, None]()

        self.onlineHandlers = FunctionHandlers[HandlerScope, None]()
        self.offlineHandlers = FunctionHandlers[HandlerScope, None]()
        self.shutdownHandlers = FunctionHandlers[HandlerScope, None]()
        self.abortHandlers = FunctionHandlers[HandlerScope, None]()
        self.stopHandlers = FunctionHandlers[HandlerScope, None]()
        self.diagnosticHandlers = FunctionHandlers[(UTCTime, str), None]()
        self.operationsHandlers = FunctionHandlers[HandlerScope, None]()
        self.exceptionHandlers = FunctionHandlers[Exception, None]()
        self.newSequenceHandlers = FunctionHandlers[HandlerScope, None]()

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

    def _defaultCommandHandler(self, input: SequenceCommand):
        print(f"Error: Command with: ${input.commandName.name} is not handled by the loaded sequencer script")
        raise TypeError

    def execute(self, command: SequenceCommand):
        if isinstance(command, Setup):
            s: Setup = command
            if self.setupCommandHandler.contains(s.commandName.name):
                self.setupCommandHandler.execute(s.commandName.name, s)
        elif isinstance(command, Observe):
            o: Observe = command
            if self.observerCommandHandler.contains(o.commandName.name):
                self.observerCommandHandler.execute(o.commandName.name, o)
        else:
            self._defaultCommandHandler(command)

    def _executeHandler[T](self, f: FunctionHandlers[T, None], arg: T):
        return f.execute(arg)

    def executeGoOnline(self):
        """
        Executes the script's onGoOnline handler
        """
        self._executeHandler(self.onlineHandlers, None)
        self.isOnline = True

    def executeGoOffline(self):
        """
        Executes the script's onGoOffline handler
        """
        self._executeHandler(self.offlineHandlers, None)
        self.isOnline = False

    def executeShutdown(self):
        """
        Executes the script's onShutdown handler
        """
        self._executeHandler(self.shutdownHandlers, None)
        # self.shutdownTask.run

    def executeNewSequenceHandler(self):
        """
        Executes the script's onNewSequence handler
        """
        self._executeHandler(self.newSequenceHandlers, None)

    def executeAbort(self):
        """
        Executes the script's onAbortSequence handler
        """
        self._executeHandler(self.abortHandlers, None)

    def executeStop(self):
        """
        Executes the script's onStop handler
        """
        self._executeHandler(self.stopHandlers, None)

    def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Executes the script's onDiagnosticMode handler
        """
        self.diagnosticHandlers.execute((startTime, hint))

    def executeOperationsMode(self):
        """
        Executes the script's onOperationsMode handler
        """
        self._executeHandler(self.operationsHandlers, None)

    def executeExceptionHandlers(self, ex: Exception):
        """
        Executes the script's onException handler
        """
        self._executeHandler(self.exceptionHandlers, ex)

    def shutdownScript(self):
        """
        Runs the shutdown runnable(some extra tasks while unloading the script)
        """
        # shutdownTask.run
        pass

    # XXX TODO: Use async
    def _nextIf(self, f: Callable[[SequenceCommand], bool]) -> SequenceCommand | None:
        operator = self.sequenceOperatorFactory()
        mayBeNext = operator.maybeNext()
        match mayBeNext:
            case Step() if f(mayBeNext.command):
                nextStep = operator.pullNext()
                match nextStep:
                    case PullNextResult():
                        x: PullNextResult = nextStep
                        return x.step.command
                    case Unhandled():
                        return None
            case None:
                return None

    def onSetupCommand(self, name: str, handler: CommandHandler):
        return self.setupCommandHandler.add(name, handler.execute)

    def onObserveCommand(self, name: str, handler: CommandHandler):
        return self.observerCommandHandler.add(name, handler.execute)

    def onGoOnline(self, handler: Callable[[HandlerScope], None]):
        return self.onlineHandlers.add(handler)

    def onNewSequence(self, handler: Callable[[HandlerScope], None]):
        return self.newSequenceHandlers.add(handler)

    def onAbortSequence(self, handler: Callable[[HandlerScope], None]):
        return self.abortHandlers.add(handler)

    def onStop(self, handler: Callable[[HandlerScope], None]):
        return self.stopHandlers.add(handler)

    def onShutdown(self, handler: Callable[[HandlerScope], None]):
        return self.shutdownHandlers.add(handler)

    def onGoOffline(self, handler: Callable[[HandlerScope], None]):
        return self.offlineHandlers.add(handler)

    def onDiagnosticMode(self, handler: Callable[[(UTCTime, str)], None]):
        return self.diagnosticHandlers.add(handler)

    def onOperationsMode(self, handler: Callable[[HandlerScope], None]):
        return self.operationsHandlers.add(handler)

    def onException(self, handler: Callable[[Exception], None]):
        return self.exceptionHandlers.add(handler)
