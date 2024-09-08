from dataclasses import dataclass

import pytest

from sequencer.FunctionHandlers import FunctionHandlers


def test_FunctionHandlers1():
    "Must return empty buffer when handlers are empty | ESW-90"
    functionHandlers = FunctionHandlers[int, str]()
    assert len(functionHandlers.execute(1)) == 0

def test_FunctionHandlers2():
    "Must return output in order when handlers are added | ESW-90"
    functionHandlers = FunctionHandlers[int, int]()
    functionHandlers.add(lambda number: number + 10)
    functionHandlers.add(lambda number: number - 10)
    functionHandlers.add(lambda number: number * 2)
    assert(functionHandlers.execute(100) == [110, 90, 200])

def test_FunctionHandlers3():
    "Must throw an exception when one of the handler fails | ESW-90"
    functionHandlers = FunctionHandlers[int, int]()
    functionHandlers.add(lambda number: number + 10)
    functionHandlers.add(lambda number: number / 0)
    functionHandlers.add(lambda number: number * 2)
    with pytest.raises(Exception):
        functionHandlers.execute(100)
