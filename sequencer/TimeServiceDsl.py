from datetime import timedelta
from typing import Callable, Awaitable

import structlog

from csw.Cancellable import Cancellable
from csw.TMTTime import TAITime
from csw.TMTTime import TMTTime
from csw.TimeServiceScheduler import TimeServiceScheduler
from csw.TMTTime import UTCTime


class TimeServiceDsl:
    """
    Python Dsl for scheduling periodic/non-periodic tasks at a specified time and/or interval.
    This Dsl provides simplified APIs over csw time service dsl, and some utility methods for scripts.
    It supports scheduling on both UTCTime and TAITime.
    Each API returns a Cancellable which allows users to cancel the execution of tasks.
    """
    log = structlog.get_logger()

    def __init__(self):
        self.timeService = TimeServiceScheduler()

    def scheduleOnce(self, startTime: TMTTime, func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules an async function to execute once at the given start time.

        Args:
            startTime: the time at which the task should start its execution
            func: the async function (coroutine) to be scheduled for execution

        Returns:
            a handle to cancel the execution of the task if it hasn't been executed already
        """
        return self.timeService.scheduleOnce(startTime, func)

    def scheduleOnceFromNow(self, delayFromNow: timedelta, func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules function once at duration after current utc time.

        Args:

            delayFromNow: delay after which task will be scheduled as a timedelta
            func: the function to be scheduled for execution

        Returns:
            a handle to cancel the execution of the function if it hasn't been executed already
        """
        return self.scheduleOnce(self.utcTimeAfter(delayFromNow), func)

    def schedulePeriodicallyStarting(self, startTime: TMTTime, interval: timedelta,
                                     func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules a task to execute periodically at the given interval. The task is executed once at the given start time followed by execution of task at each interval.

        Args:
            startTime: first time at which task is to be executed
            interval: the time interval between the execution of tasks
            func: the task to execute after each interval

        Returns:
            a handle to cancel the execution of further tasks
        """
        return self.timeService.schedulePeriodicallyStarting(startTime, interval, func)

    def schedulePeriodically(self, interval: timedelta, func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules a task to execute periodically at the given interval.
        The task is executed immediately and then after every provided duration.

        Args:
            interval: the time interval between the execution of tasks
            func: the task to execute after each interval

        Returns:
            a handle to cancel the execution of further tasks
        """
        return self.timeService.schedulePeriodically(interval, func)

    def schedulePeriodicallyFromNow(self, delayFromNow: timedelta, interval: timedelta,
                                    func: Callable[[], Awaitable]) -> Cancellable:
        """
        Schedules a task to execute periodically at the given interval. The task is executed once at duration after current utc time
        followed by execution of task at each interval.

        Args:
            delayFromNow: delay after which the first task will be scheduled as a timedelta
            interval: the time interval between the execution of tasks
            func: the task to execute after each interval

        Returns:
            a handle to cancel the execution of further tasks
        """
        return self.timeService.schedulePeriodicallyStarting(self.utcTimeAfter(delayFromNow), interval, func)

    def utcTimeNow(self) -> UTCTime:
        """
        Utility to calculate current UTC time

        Returns:
            current UTC time
        """
        return UTCTime.now()

    def taiTimeNow(self) -> TAITime:
        """
        Utility to calculate current TAI time

        Returns:
            current TAI time
        """
        return TAITime.now()

    def utcTimeAfter(self, duration: timedelta) -> UTCTime:
        """
        Utility to calculate UTC time after specified duration

        Args:
            duration: time duration

        Returns:
            UTC time after specified time duration
        """
        return UTCTime.after(duration)

    def taiTimeAfter(self, duration: timedelta) -> TAITime:
        """
        Utility to calculate TAI time after specified duration

        Args:
            duration: time duration

        Returns:
            TAI time after specified time duration
        """
        return TAITime.after(duration)

