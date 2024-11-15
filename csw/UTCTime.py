from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Self

from dateutil import parser

@dataclass
class UTCTime:
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
    def _asDict(self):
        return asdict(self)

    @classmethod
    def _fromDict(cls, obj: dict) -> Self:
        return cls(**obj)

    @staticmethod
    def from_str(timeStr: str):
        """
        Returns a UTCTime given a string in ISO format (ex: "2021-09-20T18:44:12.419084072Z").
        """
        t = parser.isoparse(timeStr).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return UTCTime(seconds, nanos)

    @staticmethod
    def now():
        """
        Returns a UTCTime with the current time.
        """
        t = datetime.now(timezone.utc).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return UTCTime(seconds, nanos)
