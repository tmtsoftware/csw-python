from time import sleep
from typing import List

from csw.CommandResponse import Started, Completed
from csw.Event import Event
from csw.ExposureId import ExposureId
from csw.ObsId import ObsId
from csw.ParameterSetType import Observe, Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from esw.ObsMode import ObsMode
from sequencer.Script import Script
from sequencer.examples.testData.InitialCommandHandler import InitialCommandHandler


def script(ctx: Script):
    lgsfSequencer = ctx.Sequencer(Subsystem.LGSF, ObsMode("darknight"))
    testAssembly = ctx.Assembly(Prefix(Subsystem.ESW, "test"), 10)

    # ESW-134: Reuse code by ability to import logic from one script into another
    InitialCommandHandler(ctx)

    ctx.onSetup("command-2", lambda setup: print(f"Received a command-2 setup: {setup}"))

    # ESW-421 demonstrate creating exposureId and obsId. Getting components from exposureId and ObsId
    def _handleExposureStart(_: Observe):
        obsId = ObsId.make("2021A-011-153")
        # do something with ObsId components
        print(obsId.programId)
        print(obsId.programId.semesterId)
        print(obsId.programId.semesterId.semester)

        # create exposureId
        exposureIdStr = f"{obsId}-TCS-DET-SCI0-0001"
        exposureId = ExposureId.make(exposureIdStr)
        # do something with exposureId components
        print(exposureId.subsystem)
        print(exposureId.det)
        ctx.publishEvent(ctx.exposureStart(exposureId))

    ctx.onObserve("exposure-start", _handleExposureStart)

    ctx.onSetup("command-3", lambda setup: print(f"Received a command-3 setup: {setup}"))

    def _handleCommand4(_: Setup):
        # try sending concrete sequence
        setupCommand = ctx.Setup("ESW.test", "command-3")
        sequence = ctx.sequenceOf(setupCommand)

        # ESW-88, ESW-145, ESW-195
        tcsSequencer = ctx.Sequencer(Subsystem.TCS, ObsMode("darknight"))
        tcsSequencer.submitAndWait(sequence, 10)

    ctx.onSetup("command-4", _handleCommand4)

    def _handleCheckConfig(_: Setup):
        if ctx.existsConfig("/tmt/test/wfos.conf"):
            ctx.publishEvent(ctx.SystemEvent("WFOS.test", "check-config.success"))

    ctx.onSetup("check-config", _handleCheckConfig)

    # XXX TODO
    # def _handleGetConfigData(setup: Setup):
    #     configValue = "component = wfos"
    #     configData = ctx.getConfig("/tmt/test/wfos.conf")
    #
    #     onSetup("get-config-data") {
    #         val configValue = "component = wfos"
    #         val configData = getConfig("/tmt/test/wfos.conf")
    #         configData?.let {
    #             if (it == ConfigFactory.parseString(configValue))
    #                 publishEvent(SystemEvent("WFOS.test", "get-config.success"))
    #         }
    #     }

    def _handleGetEvent(_: Setup):
        # ESW-88
        event = ctx.getEvent("ESW.test.get.event")
        successEvent = ctx.SystemEvent("ESW.test", "get.success")
        if not event.isInvalid():
            ctx.publishEvent(successEvent)

    ctx.onSetup("get-event", _handleGetEvent)

    def _handleOnEvent(_: Setup):
        def handleEvent(event: Event):
            successEvent = ctx.SystemEvent("ESW.test", "onevent.success")
            if not event.isInvalid():
                ctx.publishEvent(successEvent)

        ctx.onEvent(handleEvent, "ESW.test.get.event")

    ctx.onSetup("on-event", _handleOnEvent)

    def _handleCommandForAssembly(command: Setup):
        submitResponse = testAssembly.submit(ctx.Setup(str(command.source), "long-running"))
        if isinstance(testAssembly.query(submitResponse.runId()), Started):
            ctx.publishEvent(ctx.SystemEvent("tcs.filter.wheel", "query-started-command-from-script"))

        if isinstance(testAssembly.queryFinal(submitResponse.runId(), 100), Completed):
            ctx.publishEvent(ctx.SystemEvent("tcs.filter.wheel", "query-completed-command-from-script"))

        testAssembly.subscribeCurrentState(["stateName1", "stateName2"],
                                           lambda currentState: ctx.publishEvent(ctx.SystemEvent(
                                               "tcs.filter.wheel",
                                               f"publish-{currentState.stateName().name()}")))
        testAssembly.oneway(command)

    ctx.onSetup("command-for-assembly", _handleCommandForAssembly)


    ctx.onSetup("test-sequencer-hierarchy", lambda _: sleep(5))

    def _handleCheckException(_: Setup):
        raise Exception("boom")

    ctx.onSetup("check-exception-1", _handleCheckException)
    ctx.onSetup("check-exception-2", lambda _: sleep(0))

# XXX TODO
#     onSetup("set-alarm-severity") {
#         val alarmKey = AlarmKey(Prefix("NFIRAOS.trombone"), "tromboneAxisHighLimitAlarm")
#         setSeverity(alarmKey, Major)
#         delay(500)
#     }

    def _handleCommandLgsf(_: Setup):
        # NOT update command response to avoid a sequencer to finish immediately
        # so that others Add, Append command gets time
        setupCommand = ctx.Setup("LGSF.test", "command-lgsf")
        sequence = ctx.sequenceOf(setupCommand)
        lgsfSequencer.submitAndWait(sequence, 10)

    ctx.onSetup("command-lgsf", _handleCommandLgsf)

# XXX TODO
#    def _handleScheduleOnceFromNow(_: Setup):
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


    # def _handleOnDiagnosticMode(startTime, hint):
    #     # do some actions to go to diagnostic mode based on hint
    #     testAssembly.diagnosticMode(startTime, hint)

#     onOperationsMode {
#         // do some actions to go to operations mode
#         testAssembly.operationsMode()
#     }
#
#     onGoOffline {
#         // do some actions to go offline
#         testAssembly.goOffline()
#     }
#
#     onGoOnline {
#         // do some actions to go online
#         testAssembly.goOnline()
#     }
#
#     onAbortSequence {
#         //do some actions to abort sequence
#
#         //send abortSequence command to downstream sequencer
#         lgsfSequencer.abortSequence()
#     }
#
#     onStop {
#         //do some actions to stop
#
#         //send stop command to downstream sequencer
#         lgsfSequencer.stop()
#     }
#
# }
