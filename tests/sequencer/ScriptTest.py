import asyncio
import configparser
import os
from typing import Callable

import aiohttp

from csw.AlarmService import AlarmService
from csw.Event import SystemEvent, EventName
from csw.EventService import EventService
from csw.ParameterSetType import Setup, CommandName
from csw.Prefix import Prefix
from esw.ObsMode import ObsMode
from esw.SequencerClient import SequencerClient
from sequencer.CswServices import CswServices
from sequencer.Script import Script
from sequencer.ScriptContext import ScriptContext
from sequencer.ScriptLoader import ScriptLoader
from sequencer.ScriptWiring import ScriptWiring
from sequencer.SequenceOperatorApi import SequenceOperatorHttp
from sequencer.SequencerApi import SequencerApi

# Standalone test of scripting using example TestScript.py
# This requires that csw-services and esw-services are running.
async def main():
    sequencerPrefix = Prefix.from_str('ESW.darknight')
    async with aiohttp.ClientSession() as clientSession:
        sequencerApi: SequencerApi = SequencerClient(sequencerPrefix, clientSession)
        sequenceOperatorFactory: Callable[[], SequenceOperatorHttp] = lambda: SequenceOperatorHttp(sequencerApi)
        obsMode = ObsMode.fromPrefix(sequencerPrefix)
        evenService = EventService()
        alarmService = AlarmService()
        scriptContext = ScriptContext(1, sequencerPrefix, obsMode, clientSession, sequenceOperatorFactory, evenService, alarmService)
        cswServices = await CswServices.create(clientSession, scriptContext)
        scriptWiring = ScriptWiring(scriptContext, cswServices)
        script = Script(scriptWiring)
        cfg = configparser.ConfigParser()
        thisDir = os.path.dirname(os.path.abspath(__file__))
        cfg.read(f'{thisDir}/../../sequencer/examples/examples.ini')
        scriptPath = cfg.get("scripts", str(sequencerPrefix))
        scriptFile = f"{thisDir}/../../sequencer/{scriptPath}"
        module = ScriptLoader.loadPythonScript(scriptFile)

        # Run the script
        module.script(script)

        # test the script
        publisher = await scriptContext.eventService.defaultPublisher(clientSession)
        publisher.publish(SystemEvent(Prefix.from_str("esw.test"), EventName("get.event")))
        setup  = Setup(Prefix.from_str("esw.test"), CommandName("get-event"))
        await script.scriptDsl.execute(setup)

        print("XXX done")

if __name__ == "__main__":
    asyncio.run(main())
