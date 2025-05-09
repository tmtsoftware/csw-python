import asyncio
from typing import Awaitable, Callable


async def par(*func: Callable[[], Awaitable]) -> list:
    """
    Executes provided functions in parallel and waits for all of them to complete.

    Args:
        one or more async functions to run

    Returns:
         a list of responses when all the functions have completed
    """
    return await asyncio.gather(*func)
