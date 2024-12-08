import asyncio
from datetime import timedelta
from functools import wraps
from typing import Callable, Awaitable

import structlog


class LoopException(Exception):
    pass


class LoopDsl:
    log = structlog.get_logger()

    async def loop(self, func: Callable[[], Awaitable], **kwargs):
        """
        Runs the given function in a loop synchronously with the given delay.
        Use stopWhen(cond) to end loop.

        Args:
            func: The function to call
            kwargs: same keyword args as timedelta (seconds = 1, milliseconds = 50, etc.)
        """
        if len(kwargs) == 0:
            loopInterval = timedelta(milliseconds=50)
        else:
            loopInterval = timedelta(**kwargs)
        while True:
            try:
                await func()
                await asyncio.sleep(loopInterval.total_seconds())
            except LoopException:
                break

    def stopWhen(self, cond: bool):
        if cond:
            raise LoopException()

    async def waitFor(self, func: Callable[[], bool]):
        """
        Runs the given function in a loop synchronously until it returns true
        Suggested usage: waitFor(lambda: expr)

        Args:
            func: The function to call
        """
        loopInterval = 50.0/1000.0
        while True:
            if func():
                break
            await asyncio.sleep(loopInterval)

    def loopAsync(self, **kwargs):
        """
        A decorator that runs the given function in a loop asynchronously with the given delay.
        Use stopWhenAsync(cond) to end loop.

        Args:
            func: The function to call
            kwargs: same keyword args as timedelta (seconds = 1, milliseconds = 50, etc.)
        """

        def decorator(func: Callable[[], Awaitable]):
            loopInterval = timedelta(**kwargs)

            @wraps(func)
            async def wrapper():
                while True:
                    await func()
                    await asyncio.sleep(loopInterval.total_seconds())

            asyncio.create_task(wrapper())
            return wrapper

        return decorator

    def stopWhenAsync(self, cond: bool):
        """
        to be used within loop/loopAsync and breaks the loop if condition is true
        """
        if cond:
            asyncio.current_task().cancel()
