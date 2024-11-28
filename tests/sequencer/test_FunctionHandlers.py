from dataclasses import dataclass

import pytest

from sequencer.FunctionHandlers import FunctionHandlers


async def test_FunctionHandlers1():
    "Must return empty buffer when handlers are empty | ESW-90"
    functionHandlers = FunctionHandlers()
    assert len(await functionHandlers.execute(1)) == 0


async def test_FunctionHandlers2():
    "Must return output in order when handlers are added | ESW-90"
    functionHandlers = FunctionHandlers()

    async def foo1(n):
        return n + 10

    async def foo2(n):
        return n - 10

    async def foo3(n):
        return n * 2

    functionHandlers.add(foo1)
    functionHandlers.add(foo2)
    functionHandlers.add(foo3)
    assert (await functionHandlers.execute(100) == [110, 90, 200])


async def test_FunctionHandlers3():
    "Must throw an exception when one of the handler fails | ESW-90"
    functionHandlers = FunctionHandlers()

    async def foo1(n):
        return n + 10

    async def foo2(n):
        return n / 0

    async def foo3(n):
        return n * 2

    functionHandlers.add(foo1)
    functionHandlers.add(foo2)
    functionHandlers.add(foo3)
    with pytest.raises(Exception):
        await functionHandlers.execute(100)
