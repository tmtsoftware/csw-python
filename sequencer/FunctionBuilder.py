from typing import Callable, Self, Awaitable, Dict

import structlog


class FunctionBuilder[K, I, O]:
    """
    A builder class for a set of common functions.
    which holds a map where functions are kept as values against a unique key
    (being used in ScriptDsl to hold the command handlers)

    Generic types:
    K - Type of the key in the mutable map against which the function to be kept as value
    I - Type of the input param of the Function
    O - Type of the output result of the Function
   """

    def __init__(self):
        self.handlers: Dict[K, Callable[[I], Awaitable]] = {}
        self.log = structlog.get_logger()

    def add(self, key: K, handler: Callable[[I], Awaitable]):
        self.handlers[key] = handler

    def contains(self, key: K) -> bool:
        return key in self.handlers

    async def execute(self, key: K, cmd: I) -> O:
        return await self.handlers[key](cmd)

    def merge(self, that: Self) -> Self:
        self.handlers |= that.handlers
        return self
