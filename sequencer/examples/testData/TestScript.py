import asyncio

import structlog
from pyhocon import ConfigFactory

from csw.CommandResponse import Started, Completed
from csw.CurrentState import CurrentState
from csw.Event import Event, SystemEvent, EventName
from csw.ExposureId import ExposureId
from csw.ObsId import ObsId
from csw.ParameterSetType import Observe, Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from csw.UTCTime import UTCTime
from esw.ObsMode import ObsMode
from sequencer.Script import Script
from sequencer.examples.testData.InitialCommandHandler import InitialCommandHandler


def script(ctx: Script):
    log = structlog.get_logger()
    lgsfSequencer = ctx.Sequencer(Subsystem.LGSF, ObsMode("darknight"))
    testAssembly = ctx.Assembly(Prefix(Subsystem.ESW, "test"), 10)

    # ESW-134: Reuse code by ability to import logic from one script into another
    InitialCommandHandler(ctx, log)

    async def handleCommand2(setup: Setup):
        log.info(f"XXX TestScript: Received a command-2 setup: {setup}")

    ctx.onSetup("command-2", handleCommand2)

    # ESW-421 demonstrate creating exposureId and obsId. Getting components from exposureId and ObsId
    async def handleExposureStart(_: Observe):
        obsId = ObsId.make("2021A-011-153")
        # do something with ObsId components
        log.info(obsId.programId)
        log.info(obsId.programId.semesterId)
        log.info(obsId.programId.semesterId.semester)

        # create exposureId
        exposureIdStr = f"{obsId}-TCS-DET-SCI0-0001"
        exposureId = ExposureId.make(exposureIdStr)
        # do something with exposureId components
        log.info(exposureId.subsystem)
        log.info(exposureId.det)
        await ctx.publishEvent(ctx.exposureStart(exposureId))

    ctx.onObserve("exposure-start", handleExposureStart)

    async def handleCommand3(setup: Setup):
        log.info(f"XXX Received a command-3 setup: {setup}")

    ctx.onSetup("command-3", handleCommand3)

    async def handleCommand4(_: Setup):
        # try sending concrete sequence
        setupCommand = ctx.Setup("ESW.test", "command-3")
        sequence = ctx.sequenceOf(setupCommand)

        # ESW-88, ESW-145, ESW-195
        tcsSequencer = ctx.Sequencer(Subsystem.TCS, ObsMode("darknight"))
        await tcsSequencer.submitAndWait(sequence, 10)

    ctx.onSetup("command-4", handleCommand4)

    async def handleCheckConfig(_: Setup):
        if ctx.existsConfig("/tmt/test/wfos.conf"):
            await ctx.publishEvent(ctx.SystemEvent("WFOS.test", "check-config.success"))

    ctx.onSetup("check-config", handleCheckConfig)

    async def handleGetConfigData(setup: Setup):
        configValue = "component = wfos"
        configData = ctx.getConfig("/tmt/test/wfos.conf")
        if configData:
            if str(configData) == str(ConfigFactory.parse_string(configValue)):
                await ctx.publishEvent(SystemEvent(Prefix.from_str("WFOS.test"), EventName("get-config.success")))

    ctx.onSetup("get-config-data", handleGetConfigData)

    async def handleGetEvent(s: Setup):
        # ESW-88
        event = await ctx.getEvent("ESW.test.get.event")
        successEvent = ctx.SystemEvent("ESW.test", "get.success")
        if not event.isInvalid():
            await ctx.publishEvent(successEvent)

    ctx.onSetup("get-event", handleGetEvent)

    async def handleOnEvent(_: Setup):
        async def handleEvent(event: Event):
            successEvent = ctx.SystemEvent("ESW.test", "onevent.success")
            if not event.isInvalid():
                await ctx.publishEvent(successEvent)

        await ctx.onEvent(handleEvent, "ESW.test.get.event")

    ctx.onSetup("on-event", handleOnEvent)

    async def handleCommandForAssembly(command: Setup):
        submitResponse = await testAssembly.submit(ctx.Setup(str(command.source), "long-running"))
        if isinstance(await testAssembly.query(submitResponse.runId()), Started):
            await ctx.publishEvent(ctx.SystemEvent("tcs.filter.wheel", "query-started-command-from-script"))

        if isinstance(await testAssembly.queryFinal(submitResponse.runId(), 100), Completed):
            await ctx.publishEvent(ctx.SystemEvent("tcs.filter.wheel", "query-completed-command-from-script"))

        async def handleCurrentState(currentState: CurrentState):
            await ctx.publishEvent(ctx.SystemEvent(
                "tcs.filter.wheel",
                f"publish-{currentState.stateName}"))

        testAssembly.subscribeCurrentState(["stateName1", "stateName2"], handleCurrentState)
        await testAssembly.oneway(command)

    ctx.onSetup("command-for-assembly", handleCommandForAssembly)

    async def handleTestSequencerHierarchy(_: Setup):
        await asyncio.sleep(5)

    ctx.onSetup("test-sequencer-hierarchy", handleTestSequencerHierarchy)

    async def handleCheckException1(_: Setup):
        raise Exception("boom")

    async def handleCheckException2(_: Setup):
        pass

    ctx.onSetup("check-exception-1", handleCheckException1)
    ctx.onSetup("check-exception-2", handleCheckException2)

    # XXX TODO
    #     onSetup("set-alarm-severity") {
    #         val alarmKey = AlarmKey(Prefix("NFIRAOS.trombone"), "tromboneAxisHighLimitAlarm")
    #         setSeverity(alarmKey, Major)
    #         delay(500)
    #     }

    async def handleCommandLgsf(_: Setup):
        # NOT update command response to avoid a sequencer to finish immediately
        # so that others Add, Append command gets time
        setupCommand = ctx.Setup("LGSF.test", "command-lgsf")
        sequence = ctx.sequenceOf(setupCommand)
        await lgsfSequencer.submitAndWait(sequence, 10)

    ctx.onSetup("command-lgsf", handleCommandLgsf)

    # XXX TODO
    #    def handleScheduleOnceFromNow(_: Setup):
    #        currentTime = ctx.utcTimeNow()
    #        ctx.scheduleOnceFromNow(1.seconds) {
    #             val param = longKey("offset").set(currentTime.offsetFromNow().absoluteValue.inWholeMilliseconds)
    #             publishEvent(SystemEvent("ESW.schedule.once", "offset", param))
    #       }

    #     onSetup("schedule-once-from-now") {
    #         val currentTime = utcTimeNow()
    #         scheduleOnceFromNow(1.seconds) {
    #             val param = longKey("offset").set(currentTime.offsetFromNow().absoluteValue.inWholeMilliseconds)
    #             publishEvent(SystemEvent("ESW.schedule.once", "offset", param))
    #         }
    #     }
    #
    #     onSetup("schedule-periodically-from-now") {
    #         val currentTime = utcTimeNow()
    #         var counter = 0
    #         val a = schedulePeriodicallyFromNow(1.seconds, 1.seconds) {
    #             val param = longKey("offset").set(currentTime.offsetFromNow().absoluteValue.inWholeMilliseconds)
    #             publishEvent(SystemEvent("ESW.schedule.periodically", "offset", param))
    #             counter += 1
    #         }
    #         loop {
    #             stopWhen(counter > 1)
    #         }
    #         a.cancel()
    #     }

    async def handleDiagnosticMode(startTime: UTCTime, hint: str):
        await testAssembly.diagnosticMode(startTime, hint)

    ctx.onDiagnosticMode(handleDiagnosticMode)

    async def handleOperationsMode():
        await testAssembly.operationsMode()

    ctx.onOperationsMode(handleOperationsMode)

    async def handleGoOffline():
        await testAssembly.goOffline()

    ctx.onGoOffline(handleGoOffline)

    async def handleGoOnline():
        await testAssembly.goOnline()

    ctx.onGoOnline(handleGoOnline)

    async def handleAbortSequence():
        await lgsfSequencer.abortSequence()

    # do some actions to abort sequence
    # send abortSequence command to downstream sequencer
    ctx.onAbortSequence(handleAbortSequence)

    # do some actions to stop
    # send stop command to downstream sequencer
    async def handleStop():
        await lgsfSequencer.stop()

    ctx.onStop(handleStop)
