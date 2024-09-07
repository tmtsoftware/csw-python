from dataclasses import dataclass

from sequencer.FunctionBuilder import FunctionBuilder


def test_FunctionBuilder():
    @dataclass
    class Command:
        name: str
        value: int

    functionBuilder = FunctionBuilder[str, Command, int]()
    functionBuilder.add("square", lambda cmd: cmd.value * cmd.value)
    functionBuilder.add("abs", lambda cmd: abs(cmd.value))
    functionBuilder.add("reciprocal", lambda cmd: 1 / cmd.value)

    square = Command("square", 10)
    assert functionBuilder.contains(square.name)

    absent = Command("absent", 10)
    assert not functionBuilder.contains(absent.name)

    square = Command("square", 10)
    assert functionBuilder.execute(square.name, square) == 100

    absValue = Command("abs", 25)
    assert functionBuilder.execute(absValue.name, absValue) == 25
