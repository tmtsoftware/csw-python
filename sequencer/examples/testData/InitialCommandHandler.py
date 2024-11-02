from sequencer.Script import Script


def InitialCommandHandler(ctx: Script):
    ctx.onSetup("command-1", lambda setup: print(f"Received a command-1 setup: {setup}"))
