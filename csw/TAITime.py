from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from astropy.time import Time
from dateutil import parser


@dataclass
class TAITime:
    """
    Creates a TAITime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
    """
    seconds: int
    nanos: int

    def __str__(self):
        secs = self.seconds + self.nanos / 1e9
        dt = datetime.fromtimestamp(secs, timezone.utc)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f') + "Z"

    def _asDict(self):
        return asdict(self)

    @staticmethod
    def _fromDict(obj: dict):
        return TAITime(**obj)

    @staticmethod
    def from_str(timeStr: str):
        """
        Returns a TAITime given a string in ISO format (ex: "2021-09-20T18:44:12.419084072Z").
        """
        t = parser.isoparse(timeStr).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return TAITime(seconds, nanos)

    @staticmethod
    def fromSystem():
        """
        Returns a TAITime with the current time.
        """
        t = Time.now().tai.value.timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return TAITime(seconds, nanos)
