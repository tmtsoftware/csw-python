from typing import Callable

from csw.CommandService import CommandService
from csw.Event import Event, ObserveEvent
from csw.EventPublisher import EventPublisher
from csw.ExposureId import ExposureId
from csw.LocationService import ComponentType
from csw.ParameterSetType import Setup, Observe
from csw.Prefix import Prefix
from csw.SequencerObserveEvent import SequencerObserveEvent
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

eventPublisher = EventPublisher()

sequencerObserveEvent: SequencerObserveEvent = SequencerObserveEvent(Prefix(prefix))

def publishEvent(event: Event):
    """
    Publishes the given `event`. EventServerNotAvailable when event server is not available or
    PublishFailure containing the cause for other failures.

    Args:
        event: event to publish

    Returns:
        when event is published
    """
    eventPublisher.publish(event)

def exposureStart(exposureId: ExposureId) -> ObserveEvent:
    """
    This event indicates the start of data acquisition that  results in a file produced for DMS. This is a potential metadata event for DMS.

    Args:
        exposureId: an identifier in ESW/DMS for a single exposure.
                   The ExposureId follows the structure: 2020A-001-123-WFOS-IMG1-SCI0-0001 with an included ObsId or
                    when no ObsId is present, in the standalone format: 20200706-190204-WFOS-IMG1-SCI0-0001 with a UTC time
                    when the ExposureId is created.

    Returns:
        the ObserveEvent
    """
    return sequencerObserveEvent.exposureStart(exposureId)