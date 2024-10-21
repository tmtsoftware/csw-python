from typing import Callable, Self, List


class FunctionHandlers[I, O]:
    """
    A builder class for a set of common functions

    Generic types:
    I - Type of the input param of the Function
    O - Type of the output result of the Function
   """

    def __init__(self):
        self.handlers = []

    def add(self, handler: Callable[[I], O]):
        self.handlers.append(handler)

    def execute(self, input: I) -> List[O]:
        return list(map(lambda f: f(input), self.handlers))

    def merge(self, that: Self) -> Self:
        self.handlers += that.handlers
        return self
