import structlog

from csw.ParameterSetType import Setup
from sequencer.Script import Script


def script(ctx: Script):
    log = structlog.get_logger()

    @ctx.onSetup("command-1")
    async def handleCommand1(setup: Setup):
        log.info("XXX TestScript5 received command-1")
        await ctx.publishEvent(ctx.SystemEvent("ESW.IRIS_cal", "event-1"))

