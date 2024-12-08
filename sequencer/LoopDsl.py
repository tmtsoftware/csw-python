import asyncio
from datetime import timedelta
from typing import Callable, Awaitable

import structlog

class LoopException(Exception):
    pass

class LoopDsl:
    log = structlog.get_logger()

    async def loop(self, func: Callable[[], Awaitable], **kwargs):
        """
        Runs decorated function in a loop synchronously with the given delay.
        Use stopWhen(cond) to end loop.

        Args:
            func: The function to call
            kwargs: same keyword args as timedelta (seconds = 1, milliseconds = 50, etc.)
        """
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


    # def loop(self, loopInterval: timedelta = timedelta(milliseconds=50)):
    #     """
    #     Runs a loop synchronously.
    #
    #     Args:
    #
    #     func: function to be executed on every iteration of loop until `stopWhen(condition)` written inside function becomes true.
    #     Note: loop uses default loopInterval of `50 millis`
    #
    #     loopInterval: delay between iterations of loop
    #     """
    #
    #     def decorator(func: Callable[[], Awaitable]):
    #         self.log.info("XXX in loop.decorator")
    #         @wraps(func)
    #         async def wrapper():
    #             while True:
    #                 self.log.info(f"XXX loop calling func every {loopInterval.total_seconds()}")
    #                 await func()
    #                 await asyncio.sleep(loopInterval.total_seconds())
    #
    #         self.log.info("XXX asyncio.create_task")
    #         asyncio.create_task(wrapper())
    #         return wrapper
    #
    #     return decorator

    # def loopSync(loopInterval: timedelta = timedelta(milliseconds=50)):
    #     """
    #     Runs a loop synchronously.
    #
    #     Args:
    #
    #     func: function to be executed on every iteration of loop until `stopWhen(condition)` written inside function becomes true.
    #     Note: loop uses default loopInterval of `50 millis`
    #
    #     loopInterval: delay between iterations of loop
    #     """
    #
    #     def decorator(func: Callable):
    #         async def wrapper():
    #             while True:
    #                 print(f"XXX loopSync calling func every {loopInterval.total_seconds()}")
    #                 func()
    #                 await asyncio.sleep(loopInterval.total_seconds())
    #
    #         asyncio.create_task(wrapper())
    #         return wrapper
    #
    #     return decorator


    # def stopWhen(self, cond: bool):
    #     """
    #     to be used within loop/loopAsync and breaks the loop if condition is true
    #     """
    #     if cond:
    #         asyncio.current_task().cancel()
