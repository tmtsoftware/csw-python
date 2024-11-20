import asyncio

import structlog

from csw.Parameter import stringKey
from csw.ParameterSetType import Setup
from sequencer.Script import Script


def script(ctx: Script):
    log = structlog.get_logger()

    async def handleNewSequence():
        newSequenceHandlerParam = stringKey("onNewSequence").set("Started")
        event = ctx.SystemEvent("LGSF.darknight", "NewSequenceHandler", newSequenceHandlerParam)
        ctx.publishEvent(event)
        await asyncio.sleep(0.5)

    ctx.onNewSequence(handleNewSequence)

    async def handleCommand1(_: Setup):
        log.info("XXX TestScript4 received command-1")
        newSequenceParam = stringKey("sequence-command-1").set("Started")
        event = ctx.SystemEvent("LGSF.darknight", "command1", newSequenceParam)
        ctx.publishEvent(event)

    ctx.onSetup("command-1", handleCommand1)

    async def handleCommandLgsf(_: Setup):
        # NOT update command response To avoid sequencer to
        # finish so that other commands gets time
        log.info("XXX TestScript4 Received command-lgsf")
        await asyncio.sleep(1.0)

    ctx.onSetup("command-lgsf", handleCommandLgsf)

    async def handleAbortSequence():
        # do some actions to abort sequence
        log.info("XXX TestScript4: handleAbortSequence")
        successEvent = ctx.SystemEvent("TCS.test", "abort.success")
        ctx.publishEvent(successEvent)

    ctx.onAbortSequence(handleAbortSequence)

    async def handleStop():
        # do some actions to stop
        successEvent = ctx.SystemEvent("TCS.test", "stop.success")
        ctx.publishEvent(successEvent)

    ctx.onStop(handleStop)

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
