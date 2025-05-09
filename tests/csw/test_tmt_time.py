from datetime import datetime, timezone, timedelta

from csw.TMTTime import TimeConstants, UTCTime

jitter = 100


def test1():
    """should convert utc to tai | DEOPSCSW-549"""
    utcTime = UTCTime.now()
    taiTime = utcTime.toTAI()
    diff = taiTime.value() - utcTime.value()
    assert diff.total_seconds() == TimeConstants.taiOffset


def test2():
    """should give time duration between given timestamp and current time | DEOPSCSW-549"""
    futureTime = UTCTime.after(timedelta(seconds=1))
    diff = futureTime.durationFromNow().total_seconds()
    assert abs(diff - 1.0) * 1000 < jitter


def test3():
    """should give time duration between given timestamp and current time | DEOPSCSW-549"""
    tenSeconds = timedelta(seconds=10)
    futureTime = UTCTime.after(tenSeconds)
    assert abs(futureTime.durationFromNow().total_seconds() * 1000 - tenSeconds.total_seconds() * 1000) < jitter
