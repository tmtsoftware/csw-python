from dataclasses import dataclass
from typing import Callable

from csw.AlarmService import AlarmService
from csw.EventService import EventService
from csw.Prefix import Prefix
from esw.ObsMode import ObsMode
from sequencer.SequencerApi import SequencerApi


@dataclass
class ScriptContext:
    """
    A context class created to pass following states to sequencer script
    
    Args:
        heartbeatIntervalSecs: heart beat for health check
        prefix: prefix of the sequencer
        obsMode: obsMode of the sequencer
        logger: for logging
        XXX? sequenceOperatorFactory: sequenceOperatorFactory
        eventService: an instance of EventService
        alarmService: an instance of AlarmService
        XXX? sequencerApiFactory: a Factory method to create an instance of sequencerApi
        XXX? config: overall config
    """
    heartbeatIntervalSecs: int
    prefix: Prefix
    obsMode: ObsMode
    sequenceOperatorFactory: Callable[[], SequencerApi]
    eventService: EventService
    alarmService: AlarmService
    # sequencerApiFactory: Callable[[Subsystem, ObsMode, Variation], SequencerApi]
    # config: Config
