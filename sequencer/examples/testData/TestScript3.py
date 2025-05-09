from datetime import timedelta

from csw.Parameter import stringKey
from csw.ParameterSetType import Setup
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from csw.TMTTime import UTCTime
from esw.ObsMode import ObsMode
from sequencer.Script import Script


def script(ctx: Script):
    sequencer = ctx.Sequencer(Subsystem.ESW, ObsMode("moonnight"))

    @ctx.onSetup("command-1")
    async def handleCommand1(command: Setup):
        # submit sequence to ESW.moonnight sequencer which is running in simulation mode
        submitResponse = await sequencer.submitAndWait(ctx.sequenceOf(command))

        # create an event to publish on completed submit response
        submitParam = stringKey("response").set("Completed")
        event = ctx.SystemEvent("ESW.moonnight", "submitAndWait", submitParam)

        # publishing event if submitResponse from simulation sequencer is completed
        if submitResponse.isCompleted():
            await ctx.publishEvent(event)

    @ctx.onSetup("command-2")
    async def handleCommand2(command: Setup):
        pass

    @ctx.onNewSequence()
    async def handleNewSequence():
        print("in the new sequence handler")

    @ctx.onDiagnosticMode()
    async def handleDiagnosticMode(startTime: UTCTime, hint: str):
        # do some actions to go to diagnostic mode based on hint
        diagnosticModeParam = stringKey("mode").set("diagnostic")
        event = ctx.SystemEvent("TCS.test", "diagnostic-data", diagnosticModeParam)
        await ctx.publishEvent(event)

    @ctx.onOperationsMode()
    async def handleOperationsMode():
        # do some actions to go to operations mode
        operationsModeParam = stringKey("mode").set("operations")
        event = ctx.SystemEvent("TCS.test", "diagnostic-data", operationsModeParam)
        await ctx.publishEvent(event)

    @ctx.onGoOnline()
    async def handleGoOnline():
        onlineParam = stringKey("mode").set("online")
        event = ctx.SystemEvent("TCS.test", "online", onlineParam)
        await ctx.publishEvent(event)

    @ctx.onGoOffline()
    async def handleGoOffline():
        offlineParam = stringKey("mode").set("offline")
        event = ctx.SystemEvent("TCS.test", "offline", offlineParam)
        await ctx.publishEvent(event)

    @ctx.onSetup("multi-node")
    async def handleCommand2(command: Setup):
        assembly = ctx.Assembly(Prefix(Subsystem.ESW, "SampleAssembly"), timedelta(seconds = 10))
        await assembly.submit(command)
