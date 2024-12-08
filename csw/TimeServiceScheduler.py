import asyncio
from asyncio import TimerHandle, Task
from datetime import timedelta
from typing import Callable, Awaitable

import structlog

from csw.Cancellable import Cancellable
from csw.TMTTime import TMTTime, UTCTime


class TimerCancellable(Cancellable):
    def __init__(self, timerHandle: TimerHandle | None, task: Task | None):
        self.timerHandle = timerHandle
        self.task = task

    def cancel(self) -> bool:
        if self.timerHandle:
            self.timerHandle.cancel()
        if self.task:
            self.task.cancel()
        return True


# noinspection PyTypeChecker
class TimeServiceScheduler:
    """
    Scheduler for scheduling periodic/non-periodic tasks at a specified time and/or interval.
    It supports scheduling on both UTCTime and TAITime.
    Each API returns a Cancellable which allows users to cancel the execution of tasks.
    Please note that implementation of Scheduler is optimised for high-throughput
    and high-frequency events. It is not to be confused with long-term schedulers such as Quartz.
    """

    log = structlog.get_logger()

    def scheduleOnce(self, startTime: TMTTime, func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules an async function to execute once at the given start time.

        Args:
            startTime: the time at which the task should start its execution
            func: the async function (coroutine) to be scheduled for execution

        Returns:
            a handle to cancel the execution of the task if it hasn't been executed already
        """
        event = asyncio.Event()
        loop = asyncio.get_running_loop()
        secs = startTime.durationFromNow().total_seconds()
        timerHandle = loop.call_later(secs, lambda: event.set())

        async def wrapper():
            await event.wait()
            return await func()

        task = asyncio.create_task(wrapper())
        return TimerCancellable(timerHandle, task)

    def schedulePeriodically(self, interval: timedelta, func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules a function to execute periodically at the given interval.
        The function is executed once immediately without any initial delay followed by periodic executions.
        In case you do not want to start scheduling immediately, you can use the overloaded method for `schedulePeriodically` with startTime.

        Args:
            interval: the time interval between the executions of the function
            func: the function to execute at each interval

        Returns:
            a handle to cancel execution of further tasks
        """
        secs = interval.total_seconds()

        async def periodic():
            while True:
                await func()
                await asyncio.sleep(secs)

        task = asyncio.create_task(periodic())
        return TimerCancellable(None, task)

    def schedulePeriodicallyStarting(self, startTime: TMTTime, interval: timedelta,
                             func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules a function to execute periodically at the given interval.
        The task is executed once at the given start time followed by execution of task at each interval.

        Args:
            startTime: first time at which task is to be executed
            interval: the time interval between the executions of the function
            func: the function to execute at each interval

        Returns:
            a handle to cancel execution of further tasks
        """
        startSecs = startTime.durationFromNow().total_seconds()
        secs = interval.total_seconds()
        event = asyncio.Event()
        loop = asyncio.get_running_loop()

        async def periodic():
            await event.wait()
            while True:
                await func()
                await asyncio.sleep(secs)

        timerHandle = loop.call_later(startSecs, lambda: event.set())
        task = asyncio.create_task(periodic())
        return TimerCancellable(timerHandle, task)
