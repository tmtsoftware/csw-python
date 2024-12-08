import asyncio
from datetime import timedelta

from csw.TimeServiceScheduler import TimeServiceScheduler
from csw.TMTTime import UTCTime


async def test_schedule_once():
    """
    Schedule function foo at fixed time
    """
    start = UTCTime.now()
    t = UTCTime.after(timedelta(seconds=2))
    end: UTCTime | None = None

    async def foo():
        nonlocal end
        end = UTCTime.now()

    c = TimeServiceScheduler().scheduleOnce(t, foo)
    await asyncio.sleep(2.5)
    diff = end.value() - start.value()
    assert abs(diff.total_seconds() - 2) < 0.01


async def test_schedule_once_and_cancel():
    """
    Schedule function foo at fixed time and cancel before
    """
    start = UTCTime.now()
    t = UTCTime.after(timedelta(seconds=2))
    end: UTCTime = start

    async def foo():
        nonlocal end
        end = UTCTime.now()

    c = TimeServiceScheduler().scheduleOnce(t, foo)
    await asyncio.sleep(1)
    c.cancel()
    diff = end.value() - start.value()
    assert diff.total_seconds() == 0


async def test_schedule_periodically():
    """
    Schedule function foo to run once per second, then cancel
    """
    count = 0

    async def foo():
        nonlocal count
        count = count + 1

    c = TimeServiceScheduler().schedulePeriodically(timedelta(seconds=1), foo)
    await asyncio.sleep(5.5)
    c.cancel()
    assert count == 6


async def test_schedule_periodically_with_start_time():
    """
    Schedule function foo to run once per second after start time, then cancel
    """
    count = 0

    async def foo():
        nonlocal count
        count = count + 1

    startTime = UTCTime.after(timedelta(seconds=2))
    c = TimeServiceScheduler().schedulePeriodicallyStarting(startTime, timedelta(seconds=1), foo)
    await asyncio.sleep(5.5)
    c.cancel()
    assert count == 4
