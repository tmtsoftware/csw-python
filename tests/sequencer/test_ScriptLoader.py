import pytest

from sequencer.ScriptLoader import ScriptLoader


def test_ScriptLoader1():
    script = ScriptLoader.loadPythonScript("TestScript1.py")
    assert script.foo(42) == 42

