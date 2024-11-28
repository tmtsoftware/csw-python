import traceback
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
from typing import Self, Callable, Awaitable

from sequencer.ScriptError import ScriptError
from sequencer.SequenceOperatorApi import SequenceOperatorHttp


class ScriptDsl(ScriptApi):

    def __init__(self, sequenceOperatorFactory: Callable[[], SequenceOperatorHttp]):
        self.log = structlog.get_logger()
        self.sequenceOperatorFactory = sequenceOperatorFactory
        self.isOnline = True
        self.setupCommandHandler = FunctionBuilder[str, Setup, Awaitable]()
        self.observerCommandHandler = FunctionBuilder[str, Observe, Awaitable]()

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

    async def _defaultCommandHandler(self, input: SequenceCommand):
        self.log.error(f"Command with: ${input.commandName} is handled by the loaded sequencer script")
        raise TypeError

    async def execute(self, command: SequenceCommand):
        try:
            if isinstance(command, Setup):
                s: Setup = command
                if self.setupCommandHandler.contains(s.commandName.name):
                    return await self.setupCommandHandler.execute(s.commandName.name, s)
            elif isinstance(command, Observe):
                o: Observe = command
                if self.observerCommandHandler.contains(o.commandName.name):
                    return await self.observerCommandHandler.execute(o.commandName.name, o)
            else:
                self.log.error(f"Error: Command with: ${command.commandName.name} is not handled by the loaded sequencer script")
                return await self._defaultCommandHandler(command)
        except Exception as err:
            self.log.error(f"ScriptDsl.execute(): {err=}, {type(err)=}, command = {command}")
            traceback.print_exc()

    async def _executeHandler[T](self, f: FunctionHandlers, *args):
        return await f.execute(*args)

    async def executeGoOnline(self):
        """
        Executes the script's onGoOnline handler
        """
        await self._executeHandler(self.onlineHandlers)
        self.isOnline = True

    async def executeGoOffline(self):
        """
        Executes the script's onGoOffline handler
        """
        await self._executeHandler(self.offlineHandlers)
        self.isOnline = False

    async def executeShutdown(self):
        """
        Executes the script's onShutdown handler
        """
        await self._executeHandler(self.shutdownHandlers)
        # self.shutdownTask.run

    async def executeNewSequenceHandler(self):
        """
        Executes the script's onNewSequence handler
        """
        await self._executeHandler(self.newSequenceHandlers)

    async def executeAbort(self):
        """
        Executes the script's onAbortSequence handler
        """
        await self._executeHandler(self.abortHandlers)

    async def executeStop(self):
        """
        Executes the script's onStop handler
        """
        await self._executeHandler(self.stopHandlers)

    async def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Executes the script's onDiagnosticMode handler
        """
        await self.diagnosticHandlers.execute(startTime, hint)

    async def executeOperationsMode(self):
        """
        Executes the script's onOperationsMode handler
        """
        await self._executeHandler(self.operationsHandlers)

    async def executeExceptionHandlers(self, ex: Exception):
        """
        Executes the script's onException handler
        """
        await self._executeHandler(self.exceptionHandlers, ex)

    async def shutdownScript(self):
        """
        Runs the shutdown runnable(some extra tasks while unloading the script)
        """
        # shutdownTask.run
        await self._executeHandler(self.shutdownHandlers)

    async def _nextIf(self, f: Callable[[SequenceCommand], bool]) -> SequenceCommand | None:
        operator = self.sequenceOperatorFactory()
        mayBeNext = await(operator.maybeNext())
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
        self.setupCommandHandler.add(name, handler.execute)

    def onObserveCommand(self, name: str, handler: CommandHandler):
        self.observerCommandHandler.add(name, handler.execute)

    def onGoOnline(self, handler: Callable):
        # noinspection PyTypeChecker
        self.onlineHandlers.add(handler)

    def onNewSequence(self, handler: Callable):
        # noinspection PyTypeChecker
        self.newSequenceHandlers.add(handler)

    def onAbortSequence(self, handler: Callable):
        # noinspection PyTypeChecker
        self.abortHandlers.add(handler)

    def onStop(self, handler: Callable):
        # noinspection PyTypeChecker
        self.stopHandlers.add(handler)

    def onShutdown(self, handler: Callable):
        # noinspection PyTypeChecker
        self.shutdownHandlers.add(handler)

    def onGoOffline(self, handler: Callable):
        # noinspection PyTypeChecker
        self.offlineHandlers.add(handler)

    def onDiagnosticMode(self, handler: Callable[[UTCTime, str], Awaitable]):
        self.diagnosticHandlers.add(handler)

    def onOperationsMode(self, handler: Callable):
        # noinspection PyTypeChecker
        self.operationsHandlers.add(handler)

    def onException(self, handler: Callable[[ScriptError], Awaitable]):
        self.exceptionHandlers.add(handler)
