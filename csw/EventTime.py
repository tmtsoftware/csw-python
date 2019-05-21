import time
from dataclasses import dataclass, asdict


@dataclass
class EventTime:
    """
    Creates an EventTime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
    """
    seconds: int
    nanos: int

    def asDict(self):
        return asdict(self)

    @staticmethod
    def fromDict(obj: dict):
        return EventTime(**obj)

    @staticmethod
    def fromSystem():
        """
        Returns an EventTime with the current time.
        """
        t = time.time()
        seconds = int(t)
        nanos = int((t - seconds) * 1000000000)
        return EventTime(seconds, nanos)
