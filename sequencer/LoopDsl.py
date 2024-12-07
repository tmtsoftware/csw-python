import asyncio
from datetime import timedelta
from functools import wraps
from typing import Callable, Awaitable


def loop(loopInterval: timedelta = timedelta(milliseconds=50)):
    """
    Runs a loop synchronously.

    Args:

    func: function to be executed on every iteration of loop until `stopWhen(condition)` written inside function becomes true.
    Note: loop uses default loopInterval of `50 millis`

    loopInterval: delay between iterations of loop
    """

    def decorator(func: Callable[[], Awaitable]):
        @wraps(func)
        async def wrapper():
            while True:
                await func()
                await asyncio.sleep(loopInterval.total_seconds())

        task = asyncio.create_task(wrapper())
        return wrapper

    return decorator


def stopWhen(cond: bool):
    """
    to be used within loop/loopAsync and breaks the loop if condition is true
    """
    if cond:
        asyncio.current_task().cancel()
