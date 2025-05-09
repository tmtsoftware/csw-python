from asyncio import Task
from typing import Callable, Awaitable


class EventSubscription:
    """
    Return value from EventSubscriber.subscribe(): Can be used to unsubscribe from an event.
    """
    def __init__(self, t: Task, f: Callable[[], Awaitable]):
        self.t = t
        self.f = f

    async def unsubscribe(self):
        await self.f()
        self.t.cancel()
