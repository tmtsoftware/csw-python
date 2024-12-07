import asyncio

import structlog

from csw.Parameter import stringKey
from csw.ParameterSetType import Setup
from sequencer.Script import Script


def script(ctx: Script):
    log = structlog.get_logger()

    @ctx.onNewSequence
    async def handleNewSequence():
        newSequenceHandlerParam = stringKey("onNewSequence").set("Started")
        event = ctx.SystemEvent("LGSF.darknight", "NewSequenceHandler", newSequenceHandlerParam)
        await ctx.publishEvent(event)
        await asyncio.sleep(0.5)


    @ctx.onSetup("command-1")
    async def handleCommand1(_: Setup):
        newSequenceParam = stringKey("sequence-command-1").set("Started")
        event = ctx.SystemEvent("LGSF.darknight", "command1", newSequenceParam)
        await ctx.publishEvent(event)


    @ctx.onSetup("command-lgsf")
    async def handleCommandLgsf(_: Setup):
        # NOT update command response To avoid sequencer to
        # finish so that other commands gets time
        await asyncio.sleep(1.0)


    @ctx.onAbortSequence
    async def handleAbortSequence():
        # do some actions to abort sequence
        successEvent = ctx.SystemEvent("TCS.test", "abort.success")
        await ctx.publishEvent(successEvent)


    @ctx.onStop
    async def handleStop():
        # do some actions to stop
        successEvent = ctx.SystemEvent("TCS.test", "stop.success")
        await ctx.publishEvent(successEvent)


#     onSetup("time-service-dsl") {
#         val offset = utcTimeAfter(2.seconds).offsetFromNow()
#
#         schedulePeriodically(utcTimeAfter(5.seconds), offset) {
#             publishEvent(SystemEvent("LGSF.test", "publish.success"))
#         }
#
#         scheduleOnce(taiTimeNow()) {
#             publishEvent(SystemEvent("LGSF.test", "publish.success"))
#         }
#     }
# }
