import asyncio
from datetime import datetime, timezone
from csw.ParameterSetType import *
from csw.CommandResponse import *
from csw.Prefix import Prefix
from csw.LocationService import *
from esw.SequencerRequest import *
from csw.CommandService import *
from csw.KeyTypes import KeyTypes
from csw.Parameter import *
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
from csw.ConfigService import *

from esw.Sequence import Sequence
from esw.SequencerClient import SequencerClient
from esw.SequencerRes import *
from esw.StepList import StepList
from esw.Step import Step
from esw.StepStatus import *


def hcdCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.HCD)


def assemblyCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.Assembly)


def sequencerCommandService(prefix: str) -> CommandService:
    return CommandService(Prefix.from_str(prefix), ComponentType.Sequencer)


locationService = LocationService()

print("Wellcome to ESW Shell")
