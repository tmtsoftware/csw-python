import asyncio
from datetime import timedelta

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
from csw.TMTTime import UTCTime
from esw.ObsMode import ObsMode
from sequencer.Keys import longKey
from sequencer.Script import Script
from sequencer.examples.testData.InitialCommandHandler import InitialCommandHandler


def script(ctx: Script):
    log = structlog.get_logger()
    lgsfSequencer = ctx.Sequencer(Subsystem.LGSF, ObsMode("darknight"))
    testAssembly = ctx.Assembly(Prefix(Subsystem.ESW, "test"), 10)

    # ESW-134: Reuse code by ability to import logic from one script into another
    InitialCommandHandler(ctx, log)

    @ctx.onSetup("command-2")
    async def handleCommand2(setup: Setup):
        log.info(f"XXX TestScript: Received a command-2 setup: {setup}")

    # ESW-421 demonstrate creating exposureId and obsId. Getting components from exposureId and ObsId
    @ctx.onObserve("exposure-start")
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

    @ctx.onSetup("command-3")
    async def handleCommand3(setup: Setup):
        log.info(f"XXX Received a command-3 setup: {setup}")

    @ctx.onSetup("command-4")
    async def handleCommand4(_: Setup):
        # try sending concrete sequence
        setupCommand = ctx.Setup("ESW.test", "command-3")
        sequence = ctx.sequenceOf(setupCommand)

        # ESW-88, ESW-145, ESW-195
        tcsSequencer = ctx.Sequencer(Subsystem.TCS, ObsMode("darknight"))
        await tcsSequencer.submitAndWait(sequence, 10)

    @ctx.onSetup("check-config")
    async def handleCheckConfig(setup: Setup):
        if ctx.existsConfig("/tmt/test/wfos.conf"):
            await ctx.publishEvent(ctx.SystemEvent("WFOS.test", "check-config.success"))

    @ctx.onSetup("get-config-data")
    async def handleGetConfigData(setup: Setup):
        configValue = "component = wfos"
        configData = ctx.getConfig("/tmt/test/wfos.conf")
        if configData:
            if str(configData) == str(ConfigFactory.parse_string(configValue)):
                await ctx.publishEvent(SystemEvent(Prefix.from_str("WFOS.test"), EventName("get-config.success")))

    @ctx.onSetup("get-event")
    async def handleGetEvent(s: Setup):
        # ESW-88
        event = await ctx.getEvent("ESW.test.get.event")
        successEvent = ctx.SystemEvent("ESW.test", "get.success")
        if not event.isInvalid():
            await ctx.publishEvent(successEvent)

    @ctx.onSetup("on-event")
    async def handleOnEvent(_: Setup):
        @ctx.onEvent("ESW.test.get.event")
        async def handleEvent(event: Event):
            successEvent = ctx.SystemEvent("ESW.test", "onevent.success")
            if not event.isInvalid():
                await ctx.publishEvent(successEvent)

    @ctx.onSetup("command-for-assembly")
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

    @ctx.onSetup("test-sequencer-hierarchy")
    async def handleTestSequencerHierarchy(_: Setup):
        await asyncio.sleep(5)

    @ctx.onSetup("check-exception-1")
    async def handleCheckException1(_: Setup):
        raise Exception("boom")

    @ctx.onSetup("check-exception-2")
    async def handleCheckException2(_: Setup):
        pass

    # XXX TODO implement alarm service DSL
    #     onSetup("set-alarm-severity") {
    #         val alarmKey = AlarmKey(Prefix("NFIRAOS.trombone"), "tromboneAxisHighLimitAlarm")
    #         setSeverity(alarmKey, Major)
    #         delay(500)
    #     }

    @ctx.onSetup("command-lgsf")
    async def handleCommandLgsf(_: Setup):
        # NOT update command response to avoid a sequencer to finish immediately
        # so that others Add, Append command gets time
        setupCommand = ctx.Setup("LGSF.test", "command-lgsf")
        sequence = ctx.sequenceOf(setupCommand)
        await lgsfSequencer.submitAndWait(sequence, 10)

    @ctx.onSetup("schedule-once-from-now")
    async def handleScheduleOnceFromNow(_: Setup):
        currentTime = ctx.utcTimeNow()

        async def func():
            param = longKey("offset").set(int(currentTime.offsetFromNow().total_seconds() * 1000))
            await ctx.publishEvent(ctx.SystemEvent("ESW.schedule.once", "offset", param))

        ctx.scheduleOnceFromNow(timedelta(seconds=1), func)

    @ctx.onSetup("schedule-periodically-from-now")
    async def handleSchedulePeriodicallyFromNow(_: Setup):
        currentTime = ctx.utcTimeNow()
        counter = 0

        async def publishEvents():
            nonlocal counter
            param = longKey("offset").set(round(abs(currentTime.offsetFromNow().total_seconds() * 1000)))
            await ctx.publishEvent(ctx.SystemEvent("ESW.schedule.periodically", "offset", param))
            counter = counter + 1

        a = ctx.schedulePeriodicallyFromNow(timedelta(seconds=1), timedelta(seconds=1), publishEvents)

        async def countEvents():
            ctx.stopWhen(counter > 1)

        await ctx.loop(countEvents, milliseconds=50)

        a.cancel()

    @ctx.onDiagnosticMode()
    async def handleDiagnosticMode(startTime: UTCTime, hint: str):
        await testAssembly.diagnosticMode(startTime, hint)

    @ctx.onOperationsMode()
    async def handleOperationsMode():
        await testAssembly.operationsMode()

    @ctx.onGoOffline()
    async def handleGoOffline():
        await testAssembly.goOffline()

    @ctx.onGoOnline()
    async def handleGoOnline():
        await testAssembly.goOnline()

    # do some actions to abort sequence
    # send abortSequence command to downstream sequencer
    @ctx.onAbortSequence()
    async def handleAbortSequence():
        await lgsfSequencer.abortSequence()

    # do some actions to stop
    # send stop command to downstream sequencer
    @ctx.onStop()
    async def handleStop():
        await lgsfSequencer.stop()
