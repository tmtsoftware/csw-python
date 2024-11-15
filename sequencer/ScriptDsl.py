from types import NoneType

import structlog

from csw.ParameterSetType import Setup, Observe, SequenceCommand
from csw.UTCTime import UTCTime
from esw.EswSequencerResponse import PullNextResult, Unhandled
from esw.Step import Step
from sequencer.CommandHandler import CommandHandler
from sequencer.FunctionBuilder import FunctionBuilder
from sequencer.FunctionHandlers import FunctionHandlers
from sequencer.ScriptApi import ScriptApi
from typing import Self, Callable

from sequencer.ScriptError import ScriptError
from sequencer.SequenceOperatorApi import SequenceOperatorHttp


class ScriptDsl(ScriptApi):

    def __init__(self, sequenceOperatorFactory: Callable[[], SequenceOperatorHttp]):
        self.log = structlog.get_logger()
        self.sequenceOperatorFactory = sequenceOperatorFactory
        self.isOnline = True
        self.setupCommandHandler = FunctionBuilder[str, Setup, None]()
        self.observerCommandHandler = FunctionBuilder[str, Observe, None]()

        self.onlineHandlers = FunctionHandlers()
        self.offlineHandlers = FunctionHandlers()
        self.shutdownHandlers = FunctionHandlers()
        self.abortHandlers = FunctionHandlers()
        self.stopHandlers = FunctionHandlers()
        self.diagnosticHandlers = FunctionHandlers()
        self.operationsHandlers = FunctionHandlers()
        self.exceptionHandlers = FunctionHandlers()
        self.newSequenceHandlers = FunctionHandlers()

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

    def _executeHandler[T](self, f: FunctionHandlers, *args):
        return f.execute(*args)

    def executeGoOnline(self):
        """
        Executes the script's onGoOnline handler
        """
        self._executeHandler(self.onlineHandlers)
        self.isOnline = True

    def executeGoOffline(self):
        """
        Executes the script's onGoOffline handler
        """
        self._executeHandler(self.offlineHandlers)
        self.isOnline = False

    def executeShutdown(self):
        """
        Executes the script's onShutdown handler
        """
        self._executeHandler(self.shutdownHandlers)
        # self.shutdownTask.run

    def executeNewSequenceHandler(self):
        """
        Executes the script's onNewSequence handler
        """
        self._executeHandler(self.newSequenceHandlers)

    def executeAbort(self):
        """
        Executes the script's onAbortSequence handler
        """
        self._executeHandler(self.abortHandlers)

    def executeStop(self):
        """
        Executes the script's onStop handler
        """
        self._executeHandler(self.stopHandlers)

    def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Executes the script's onDiagnosticMode handler
        """
        self.diagnosticHandlers.execute(startTime, hint)

    def executeOperationsMode(self):
        """
        Executes the script's onOperationsMode handler
        """
        self._executeHandler(self.operationsHandlers)

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

    def onGoOnline(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.onlineHandlers.add(handler)

    def onNewSequence(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.newSequenceHandlers.add(handler)

    def onAbortSequence(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.abortHandlers.add(handler)

    def onStop(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.stopHandlers.add(handler)

    def onShutdown(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.shutdownHandlers.add(handler)

    def onGoOffline(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.offlineHandlers.add(handler)

    def onDiagnosticMode(self, handler: Callable[[UTCTime, str], None]):
        return self.diagnosticHandlers.add(handler)

    def onOperationsMode(self, handler: Callable):
        # noinspection PyTypeChecker
        return self.operationsHandlers.add(handler)

    def onException(self, handler: Callable[[ScriptError], None]):
        return self.exceptionHandlers.add(handler)
