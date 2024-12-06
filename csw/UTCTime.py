from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from typing import Self

from dateutil import parser

from csw.TMTTime import TMTTime


@dataclass
class UTCTime(TMTTime):
    """
    Creates a UTCTime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
    """
    seconds: int
    nanos: int

    def __str__(self):
        secs = self.seconds + self.nanos / 1e9
        dt = datetime.fromtimestamp(secs, timezone.utc)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"

    # --- For CBOR format ---
    # noinspection PyTypeChecker
    def _asDict(self):
        return asdict(self)

    @classmethod
    def _fromDict(cls, obj: dict) -> Self:
        return cls(**obj)

    @classmethod
    def from_str(cls, timeStr: str) -> Self:
        """
        Returns a UTCTime given a string in ISO format (ex: "2021-09-20T18:44:12.419084072Z").
        """
        t = parser.isoparse(timeStr).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return cls(seconds, nanos)

    @classmethod
    def now(cls) -> Self:
        """
        Returns a UTCTime with the current time.
        """
        t = datetime.now(timezone.utc).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return cls(seconds, nanos)

    @classmethod
    def after(cls, duration: timedelta) -> Self:
        """
        Returns a UTCTime with the current time plus the given duration.
        """
        t = datetime.now(timezone.utc).timestamp() + duration.total_seconds()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return cls(seconds, nanos)

    def value(self) -> datetime:
        secs = self.seconds + self.nanos / 1e9
        return datetime.fromtimestamp(secs, timezone.utc)


    def currentInstant(self) -> datetime:
        return datetime.now(timezone.utc)

    def durationFromNow(self) -> timedelta:
        return abs(self.currentInstant() - self.value())

