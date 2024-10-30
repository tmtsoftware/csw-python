from typing import Callable
from time import sleep

from csw.ParameterSetType import SequenceCommand, ControlCommand
from sequencer.ScriptError import ScriptError, OtherError, CommandError
from sequencer.ScriptScopes import CommandHandlerScope


class CommandHandler:
    def _defaultErrorHandler(self, err: ScriptError):
        pass

    def __init__(self, scope: CommandHandlerScope, func: Callable[[CommandHandlerScope, SequenceCommand], None]):
        self.scope: CommandHandlerScope = scope
        self.func: Callable[[CommandHandlerScope, SequenceCommand], None] = func
        self._onError: Callable[[ScriptError], None] = self._defaultErrorHandler
        self._retryCount: int = 0
        self._delayInMillis: int = 0

    def execute(self, sequenceCommand: SequenceCommand):
        localRetryCount = self._retryCount
        try:
            self.func(self.scope, sequenceCommand)
        except Exception as e:
            if isinstance(e, CommandError):
                self._onError(e)
            else:
                self._onError(OtherError(e))
            if localRetryCount > 0:
                localRetryCount -= 1
                sleep(self._delayInMillis/1000.0)
                self.execute(sequenceCommand)
            else:
                raise e
