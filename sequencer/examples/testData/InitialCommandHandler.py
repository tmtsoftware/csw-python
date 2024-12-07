from csw.ParameterSetType import Setup
from sequencer.Script import Script, onSetup


def InitialCommandHandler(ctx: Script, log):
    @onSetup("command-1")
    async def handleCommand1(setup: Setup):
        log.info(f"XXX TestScript: Received a command-1 setup: {setup}")


