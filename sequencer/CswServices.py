from typing import Self

from aiohttp import ClientSession
from attr import dataclass

from csw.AlarmService import AlarmService
from csw.ConfigService import ConfigService
from csw.EventPublisher import EventPublisher
from csw.EventService import EventService
from csw.EventSubscriber import EventSubscriber
from csw.LocationService import LocationService
from csw.TimeServiceScheduler import TimeServiceScheduler
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
    timeService: TimeServiceScheduler

    # XXX TODO
    # databaseServiceFactory: DatabaseServiceFactory

    @classmethod
    def create(cls, clientSession: ClientSession, ctx: ScriptContext) -> Self:
        alarmService = ctx.alarmService
        eventService = ctx.eventService
        eventPublisher = eventService.defaultPublisher()
        eventSubscriber = eventService.defaultSubscriber()
        locationService = LocationService(clientSession)
        configService = ConfigService(clientSession)
        timeService = TimeServiceScheduler()
        return CswServices(alarmService, eventService, eventPublisher, eventSubscriber, locationService, configService, timeService)
