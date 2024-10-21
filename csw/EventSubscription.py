from redis.client import PubSubWorkerThread


class EventSubscription:
    """
    Return value from EventSubscriber.subscribe(): Can be used to unsubscribe from an event.
    """
    def __init__(self, t: PubSubWorkerThread):
        self.t = t

    def unsubscribe(self):
        self.t.stop()
