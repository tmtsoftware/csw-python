
class EventTime:

    def __init__(self, seconds, nanos):
        """
        Creates an EventTime.

        :param int seconds: time in seconds since the epoch (1970)
        :param int nanos: offset from seconds in nanoseconds
        """

        self.seconds = seconds
        self.nanos = nanos

    @staticmethod
    def fromCbor(obj):
        """
        Returns an EventTime for the given CBOR object.
        """
        return EventTime(obj['seconds'], obj['nanos'])

