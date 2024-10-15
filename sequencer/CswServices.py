from typing import Self

from attr import dataclass

from csw.AlarmService import AlarmService
from csw.ConfigService import ConfigService
from csw.EventPublisher import EventPublisher
from csw.EventService import EventService
from csw.EventSubscriber import EventSubscriber
from csw.LocationService import LocationService
from sequencer.ScriptContext import ScriptContext


@dataclass
class CswServices:
    # XXX TODO
    # logger: ILogger
    alarmService: AlarmService
    eventService: EventService
    eventPublisher: EventPublisher
    eventSubscriber: EventSubscriber
    locationService: LocationService
    configService: ConfigService

    # XXX TODO
    # timeService: TimeServiceScheduler
    # databaseServiceFactory: DatabaseServiceFactory

    @classmethod
    def create(cls, ctx: ScriptContext) -> Self:
        alarmService = ctx.alarmService
        eventService = ctx.eventService
        eventPublisher = eventService.defaultPublisher
        eventSubscriber = eventService.defaultSubscriber
        locationService = LocationService()
        configService = ConfigService()
        return CswServices(alarmService, eventService, eventPublisher, eventSubscriber, locationService, configService)
