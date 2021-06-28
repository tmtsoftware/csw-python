from datetime import datetime,timezone
from dataclasses import dataclass, asdict
from astropy.time import Time


@dataclass
class TAITime:
    """
    Creates a TAITime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
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
        return TAITime(**obj)

    @staticmethod
    def fromSystem():
        """
        Returns a TAITime with the current time.
        """
        t = Time.now().tai.value.timestamp()
        seconds = int(t)
        nanos = int((t - seconds) * 1e9)
        return TAITime(seconds, nanos)
