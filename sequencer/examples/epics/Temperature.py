# XXX TODO: Not sure yet how to implement FSM syntax in python

# import structlog
#
# from csw.Event import SystemEvent
# from sequencer.Script import Script
# from sequencer.Keys import longKey, stringKey
#
#
# def script(ctx: Script, start: str = "INIT"):
#     log = structlog.get_logger()
#
#     # temperature Fsm states
#     OK = "OK"
#     ERROR = "ERROR"
#
#     # main script Fsm states
#     INIT = "INIT"
#     STARTED = "STARTED"
#     TERMINATE = "TERMINATE"
#
#     commandFsmEvent = ctx.SystemEvent("esw.commandFsm", "state")
#     tempFsmEvent = ctx.SystemEvent("esw.temperatureFsm", "state")
#
#     tempKey = longKey("temperature")
#     stateKey = stringKey("state")
#
#     temperatureVar = ParamVariable(0, "esw.temperature.temp", tempKey)
#
#     async def publishState(baseEvent: SystemEvent, state: str):
#         await ctx.publishEvent(baseEvent.add(stateKey.set(state)))
#
#         # temp == 30               => FINISH
#         # temp > 40 or temp < 20   => ERROR
#         # else                     => OK
#         @ctx.Fsm("TEMP", OK)
#         def temperatureFsm():
#             @ctx.state(OK)
#                 def entry():
#                     ctx.publishState(tempFsmEvent, OK)
#
#                 @ctx.on(temperatureVar.first() == 30):
#                     ctx.completeFsm()
#
#                 @ctx.on(temperatureVar.first() > 40):
#                     ctx.become(ERROR)
#
#             @ctx.state(ERROR):
#                 @ctx.entry():
#                     ctx.publishState(tempFsmEvent, ERROR)
#
#                 ctx.on(temperatureVar.first() < 40):
#                     ctx.become("OK")
#
#     temperatureVar.bind(temperatureFsm)
#
# #     /**
# #      * 1. INIT =>
# #      *      1.1 start Temperature Fsm
# #      * 2. STARTED  =>
# #      *      2.1 receive cmd and set temperature process var
# #      *      2.2 if temp > 50 then TERMINATE
# #      *      2.3 else goto 2.1
# #      * 3. TERMINATE    =>
# #      *      3.1 shutdown
# #      * 4. shutdown
# #      */
# #     state(INIT) {
# #         publishState(commandFsmEvent, INIT)
# #         temperatureFsm.start()
# #         become(STARTED)
# #     }
# #
# #     state(STARTED) {
# #         publishState(commandFsmEvent, STARTED)
# #
# #         onSetup("set-temp") { cmd ->
# #             val receivedTemp = cmd(tempKey).first
# #             publishEvent(SystemEvent("esw.temperature", "temp", tempKey.set(receivedTemp)))
# #
# #             if (receivedTemp == 30L) {
# #                 temperatureFsm.await()
# #                 publishState(tempFsmEvent, "FINISHED")
# #             }
# #
# #             if (receivedTemp > 50L) {
# #                 become("TERMINATE")
# #             }
# #         }
# #     }
# #
# #     state(TERMINATE) {
# #         publishState(commandFsmEvent, TERMINATE)
# #
# #         onObserve("wait") {
# #             delay(10000)
# #         }
# #
# #         onStop {
# #             publishState(commandFsmEvent, "Fsm:TERMINATE:STOP")
# #         }
# #     }
# #
# #     onStop {
# #         publishState(commandFsmEvent, "MAIN:STOP")
# #     }
# # }
