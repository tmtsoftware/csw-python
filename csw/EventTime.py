import time
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EventTime:
    """
    Creates an EventTime containing seconds since the epoch (1970) and the offset from seconds in nanoseconds
    """
    seconds: int
    nanos: int

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return asdict(self)

    @staticmethod
    def deserialize(obj):
        """
        Returns an EventTime for the given CBOR object.
        """
        return EventTime(obj['seconds'], obj['nanos'])

    @staticmethod
    def fromSystem():
        """
        Returns an EventTime with the current time.
        """
        t = time.time()
        seconds = int(t)
        nanos = int((t - seconds) * 1000000000)
        return EventTime(seconds, nanos)
