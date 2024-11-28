import asyncio
from typing import Callable, Awaitable
from time import sleep

from csw.CommandResponse import CommandError
from csw.ParameterSetType import SequenceCommand
from sequencer.ScriptError import OtherError


class CommandHandler:
    def _defaultErrorHandler(self, err: Exception):
        pass

    def __init__(self, func: Callable[[SequenceCommand], Awaitable]):
        self.func: Callable[[SequenceCommand], Awaitable] = func
        self._onError: Callable[[Exception], None] = self._defaultErrorHandler
        self._retryCount: int = 0
        self._delayInMillis: int = 0

    async def execute(self, sequenceCommand: SequenceCommand):
        localRetryCount = self._retryCount
        try:
            await self.func(sequenceCommand)
        except Exception as e:
            if isinstance(e, CommandError):
                self._onError(e)
            else:
                self._onError(OtherError(e))
            if localRetryCount > 0:
                localRetryCount -= 1
                await asyncio.sleep(self._delayInMillis/1000.0)
                await self.execute(sequenceCommand)
            else:
                raise e
