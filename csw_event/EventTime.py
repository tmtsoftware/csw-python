import time


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

    def serialize(self):
        """
        :return: a dictionary that can be serialized to CBOR
        """
        return {
            'seconds': self.seconds,
            'nanos': self.nanos
        }


