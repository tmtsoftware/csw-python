from csw.ParameterSetType import Setup
from sequencer.Script import Script


def script(ctx: Script):

    @ctx.onSetup("command-1")
    async def handleCommand1(setup: Setup):
        await ctx.publishEvent(ctx.SystemEvent("ESW.IRIS_cal", "event-1"))

