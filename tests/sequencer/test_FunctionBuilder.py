from dataclasses import dataclass

from sequencer.FunctionBuilder import FunctionBuilder


async def test_FunctionBuilder():
    @dataclass
    class Command:
        name: str
        value: int

    functionBuilder = FunctionBuilder[str, Command, float]()

    async def foo1(cmd: Command) -> float:
        return cmd.value * cmd.value

    async def foo2(cmd: Command) -> float:
        return abs(cmd.value)

    async def foo3(cmd: Command) -> float:
        return 1 / cmd.value

    functionBuilder.add("square", foo1)
    functionBuilder.add("abs", foo2)
    functionBuilder.add("reciprocal", foo3)

    square = Command("square", 10)
    assert functionBuilder.contains(square.name)

    absent = Command("absent", 10)
    assert not functionBuilder.contains(absent.name)

    square = Command("square", 10)
    assert await functionBuilder.execute(square.name, square) == 100

    absValue = Command("abs", 25)
    assert await functionBuilder.execute(absValue.name, absValue) == 25
