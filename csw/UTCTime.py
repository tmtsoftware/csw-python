from datetime import datetime,timezone
from dataclasses import dataclass, asdict


@dataclass
class UTCTime:
    """
    Creates a UTCTime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
    """
    seconds: int
    nanos: int

    def str(self):
        secs = self.seconds + self.nanos / 1e9
        dt = datetime.fromtimestamp(secs, timezone.utc)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

    def _asDict(self):
        return asdict(self)

    @staticmethod
    def _fromDict(obj: dict):
        return UTCTime(**obj)

    @staticmethod
    def fromSystem():
        """
        Returns a UTCTime with the current time.
        """
        t = datetime.now(timezone.utc).timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return UTCTime(seconds, nanos)
