from datetime import datetime, timedelta


class TMTTime:
    """
    Represents an instantaneous point in time.
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

    def offsetFromNow(self) -> timedelta:
        return self.durationFromNow()

    def currentInstant(self) -> datetime:
        pass