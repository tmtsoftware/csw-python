from datetime import datetime, timedelta


class TMTTime:
    """
    Represents an instantaneous point in time. Its a wrapper around `java.time.Instant`and provides nanosecond precision.
    Supports 2 timescales:
    - UTCTime for Coordinated Universal Time (UTC) and
    - TAITime for International Atomic Time (TAI)
    """
    def value(self) -> datetime:
        """
        the underlying datetime
        """
        pass

    def durationFromNow(self) -> timedelta:
        pass

    def currentInstant(self) -> datetime:
        pass