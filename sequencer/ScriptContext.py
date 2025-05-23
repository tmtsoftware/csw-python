from dataclasses import dataclass
from typing import Callable

from aiohttp import ClientSession

from csw.AlarmService import AlarmService
from csw.EventService import EventService
from csw.Prefix import Prefix
from esw.ObsMode import ObsMode
from sequencer.SequenceOperatorApi import SequenceOperatorHttp


@dataclass
class ScriptContext:
    """
    A context class created to pass following states to sequencer script
    
    Args:
        heartbeatIntervalSecs: heart beat for health check
        prefix: prefix of the sequencer
        obsMode: obsMode of the sequencer
        clientSession: used for HTTP client actions
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
    clientSession: ClientSession
    sequenceOperatorFactory: Callable[[], SequenceOperatorHttp]
    eventService: EventService
    alarmService: AlarmService
    # sequencerApiFactory: Callable[[Subsystem, ObsMode, Variation], SequencerApi]
    # config: Config
