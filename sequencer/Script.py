from typing import Callable

from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.ParameterSetType import Setup, Observe
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem
from esw.ObsMode import ObsMode
from esw.SequencerClient import SequencerClient
from esw.Variation import Variation

def onSetup(commandName: str):
    def onSetupDecorator(func: Callable[[Setup], None]):
        def addSetupHandler():
            print(f"XXX addSetupHandler for {commandName}")
        return addSetupHandler

def onObserve(commandName: str):
    def onObserveDecorator(func: Callable[[Observe], None]):
        def addObserveHandler():
            print(f"XXX addObserveHandler for {commandName}")
        return addObserveHandler

def Sequencer(subsystem: Subsystem, obsMode: ObsMode, variation: str | None = None) -> SequencerClient:
    return SequencerClient(Variation.prefix(subsystem, obsMode, variation))

def Assembly(prefix: Prefix) -> CommandService:
    return CommandService(prefix, ComponentType.Assembly)

def Hcd(prefix: Prefix) -> CommandService:
    return CommandService(prefix, ComponentType.HCD)

