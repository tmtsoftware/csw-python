import asyncio
from typing import Callable, Self, List

import structlog


class FunctionHandlers:
    """
    A builder class for a set of common functions
   """

    def __init__(self):
        self.log = structlog.get_logger()
        self.handlers: List[Callable] = []

    def add(self, handler: Callable):
        self.handlers.append(handler)

    async def execute(self, *args):
        async def call(f: Callable):
            try:
                if len(args):
                    await f(*args)
                else:
                    await f()
            except Exception as ex:
                self.log.error(f"Error calling {f}({args}): {ex}")

        listOfF = list(map(lambda f: call(f), self.handlers))
        return await asyncio.gather(*listOfF)

    def merge(self, that: Self) -> Self:
        self.handlers += that.handlers
        return self
