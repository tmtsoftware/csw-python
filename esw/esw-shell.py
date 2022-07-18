from csw.ParameterSetType import *
from csw.CommandResponse import *
from csw.Prefix import Prefix
from csw.LocationService import *
from esw.SequencerRequest import *
from csw.CommandService import *
from csw.KeyType import KeyType
from csw.Parameter import Parameter
from csw.EventSubscriber import EventSubscriber
from csw.EventPublisher import EventPublisher
from csw.Event import SystemEvent, EventName
from csw.Subsystem import Subsystems
from csw.EventKey import EventKey
from csw.TAITime import TAITime
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.Coords import *
from csw.CurrentState import CurrentState

def hcdCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.HCD)

def assemblyCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.Assembly)

def sequencerCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.Sequencer)

locationService = LocationService()

print("Wellcome to ESW Shell")