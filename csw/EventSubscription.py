from asyncio import Task


class EventSubscription:
    """
    Return value from EventSubscriber.subscribe(): Can be used to unsubscribe from an event.
    """
    def __init__(self, t: Task):
        self.t = t

    def unsubscribe(self):
        self.t.cancel()
