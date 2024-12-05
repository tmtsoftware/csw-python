import asyncio
from asyncio import TimerHandle, Task
from datetime import timedelta
from typing import Callable, Awaitable
import sched, time

from csw.Cancellable import Cancellable
from csw.TMTTime import TMTTime


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

    # def scheduleOnce(self, startTime: TMTTime, func: Callable[[], None]) -> Cancellable:
    #     """
    #     Schedules a function to execute once at the given start time.
    #
    #     Args:
    #         startTime: the time at which the task should start its execution
    #         func: the function to be scheduled for execution
    #
    #     Returns:
    #         a handle to cancel the execution of the task if it hasn't been executed already
    #     """
    #     loop = asyncio.get_running_loop()
    #     secs = startTime.durationFromNow().total_seconds()
    #     timerHandle = loop.call_at(loop.time() + secs, func)
    #     return TimerCancellable(timerHandle)

    # def _schedule_at(self, func: Callable[[], Awaitable], when: float, loop: asyncio.AbstractEventLoop = None):
    #     event = asyncio.Event()
    #     loop = loop or asyncio.get_event_loop()
    #     loop.call_at(when, lambda: event.set())
    #
    #     async def wrapper():
    #         await event.wait()
    #         return await func()
    #
    #     return asyncio.create_task(wrapper())
    #
    # def _schedule_after(self, func: Callable[[], Awaitable], delay: float, loop: asyncio.AbstractEventLoop = None):
    #     loop = loop or asyncio.get_event_loop()
    #     return self._schedule_at(func, loop.time() + delay, loop)

    async def scheduleOnce(self, startTime: TMTTime, func: Callable[[], Awaitable]) -> Cancellable:
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


    # def schedulePeriodically(interval: timedelta, func: Callable[[], None]) -> Cancellable:
    #     """
    #     Schedules a function to execute periodically at the given interval.
    #     The function is executed once immediately without any initial delay followed by periodic executions.
    #     In case you do not want to start scheduling immediately, you can use the overloaded method for `schedulePeriodically` with startTime.
    #
    #     Args:
    #         interval: the time interval between the executions of the function
    #         func: the function to execute at each interval
    #
    #     Returns:
    #         a handle to cancel execution of further tasks
    #     """
    #     func()
    #     loop = asyncio.get_running_loop()
    #     secs = interval.total_seconds()
    #     def wrapper():
    #         func()
    #     timerHandle = loop.call_at(loop.time() + secs, func)
    #     return TimerCancellable(timerHandle)


    async def schedulePeriodically(interval: timedelta, func: Callable[[], Awaitable]) -> Cancellable:
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

#   /**
#    * Schedules a task to execute periodically at the given interval. The task is executed once immediately without any initial delay.
#    * In case you do not want to start scheduling immediately, you can use the overloaded method for `schedulePeriodically` with startTime.
#    *
#    * @param interval the time interval between the execution of tasks
#    * @param task the task to execute at each interval
#    * @return a handle to cancel execution of further tasks
#    */
#   def schedulePeriodically(interval: Duration, task: Runnable): Cancellable
#
#   /**
#    * Sends message to the given actor periodically at the given interval. The first message is sent immediately without any initial delay.
#    * In case you do not want to start sending immediately, you can use the overloaded method for `schedulePeriodically` with startTime.
#    *
#    * @param interval the time interval between messages sent to the actor
#    * @param receiver the actorRef to notify at each interval
#    * @param message the message to send to the actor
#    * @return a handle to cancel sending further messages
#    */
#   def schedulePeriodically(interval: Duration, receiver: ActorRef, message: Any): Cancellable
#
#   /**
#    * Schedules a task to execute periodically at the given interval. The task is executed once at the given start time followed by execution of task at each interval.
#    *
#    * @param startTime first time at which task is to be executed
#    * @param interval the time interval between the execution of tasks
#    * @param task the task to execute after each interval
#    * @return a handle to cancel execution of further tasks
#    */
#   def schedulePeriodically(startTime: TMTTime, interval: Duration)(task: => Unit): Cancellable
#
#   /**
#    * Schedules a task to execute periodically at the given interval. The task is executed once at the given start time followed by execution of task at each interval.
#    *
#    * @param startTime first time at which task is to be executed
#    * @param interval the time interval between the execution of tasks
#    * @param task the task to execute after each interval
#    * @return a handle to cancel the execution of further tasks
#    */
#   def schedulePeriodically(startTime: TMTTime, interval: Duration, task: Runnable): Cancellable
#
#   /**
#    * Sends message to the given actor periodically at the given interval. The first message is sent at the given start time and the rest are sent at specified intervals.
#    *
#    * @param startTime time at which the first message will be sent
#    * @param interval the time interval between messages sent to the actor
#    * @param receiver the actorRef to notify at each interval
#    * @param message the message to send to the actor
#    * @return a handle to cancel sending further messages
#    */
#   def schedulePeriodically(startTime: TMTTime, interval: Duration, receiver: ActorRef, message: Any): Cancellable
# }
