from csw.ParameterSetType import CommandName, Setup, Observe
from sequencer.FunctionBuilder import FunctionBuilder
from sequencer.ScriptApi import ScriptApi


class ScriptDsl(ScriptApi):
    isOnline = True
    setupCommandHandler = FunctionBuilder[str, Setup, None]()
    observerCommandHandler = FunctionBuilder[str, Observe, None]()
