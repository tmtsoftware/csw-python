from typing import Callable

from csw.CommandService import CommandService
from csw.LocationService import ComponentType
from csw.ParameterSetType import Setup, Observe
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from esw.ObsMode import ObsMode
from esw.SequencerClient import SequencerClient
from esw.Variation import Variation

class Script():
    def onSetup(self, commandName: str, func: Callable[[Setup], None]):
        pass

    def onObserve(self, commandName: str, func: Callable[[Observe], None]):
        pass

def Sequencer(subsystem: Subsystems, obsMode: ObsMode, variation: str | None = None) -> SequencerClient:
    return SequencerClient(Variation.prefix(subsystem, obsMode, variation))

def Assembly(prefix: Prefix) -> CommandService:
    return CommandService(prefix, ComponentType.Assembly)

def Hcd(prefix: Prefix) -> CommandService:
    return CommandService(prefix, ComponentType.HCD)

# def onSetup(commandName: str, func: Callable[[], None]):
#     pass
