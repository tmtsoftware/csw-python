from typing import Callable

from multipledispatch import dispatch

from csw.Event import EventName, SystemEvent, Event
from csw.EventKey import EventKey
from csw.EventPublisher import EventPublisher
from csw.EventSubscriber import EventSubscriber
from csw.EventSubscription import EventSubscription
from csw.Parameter import Parameter
from csw.Prefix import Prefix


class EventServiceDsl:

    def __init__(self):
        self.eventPublisher = EventPublisher()
        self.eventSubscriber = EventSubscriber()

    @dispatch(str, str)
    def EventKey(self, prefix: str, eventName: str) -> EventKey:
        """
        Method to create an instance of EventKey

        Args:
            prefix of the component which publishes this event
            eventName represents the name of the event

        Returns:
            an instance of EventKey
        """
        return EventKey(Prefix.from_str(prefix), EventName(eventName))

    @dispatch(str)
    def EventKey(self, eventKeyStr: str) -> EventKey:
        """
        Method to create an instance of EventKey

        Args:
            eventKeyStr string representation of event key

        Returns:
            an instance of EventKey
        """
        return EventKey.from_str(eventKeyStr)

    def SystemEvent(self, sourcePrefix: str, eventName: str, *parameters: Parameter) -> SystemEvent:
        """
        Method to create an instance of SystemEvent

        Args:
            sourcePrefix: prefix of the component which publishes this event
            eventName: represents the name of the event
            parameters: parameters to be added in the event
        """
        return SystemEvent(Prefix.from_str(sourcePrefix), EventName(eventName), list(parameters))

    @dispatch(Event)
    def publishEvent(self, event: Event):
        """
        Publishes the given `event`.

        Args:
            event: event to publish
        """
        self.eventPublisher.publish(event)

    # XXX TODO
    #     /**
    #      * Publishes the event generated by `eventGenerator` at `every` frequency. Cancellable can used to
    #      * stop the publishing. Throws [[csw.event.api.exceptions.EventServerNotAvailable]] when event server is not available or
    #      * [[csw.event.api.exceptions.PublishFailure]] containing the cause for other failures.
    #      *
    #      * @param every frequency with which the events are to be published
    #      * @param eventGenerator function which will be called at given frequency to generate an event to be published
    #      * @return handle of [[org.apache.pekko.actor.Cancellable]] which can be used to stop event publishing
    #      */
    #     fun publishEvent(every: Duration, eventGenerator: SuspendableSupplier<Event?>): Cancellable =
    #             eventPublisher.publishAsync({
    #                 coroutineScope.future { Optional.ofNullable(eventGenerator()) }
    #             }, every.toJavaDuration())

    def onEvent(self, *eventKeys: str, callback: Callable[[Event], None]) -> EventSubscription:
        """
        Subscribes to the `eventKeys` which will execute the given `callback` whenever an event is published on any one of the event keys.

        Args:
            *eventKeys: collection of strings representing EventKey
            callback: callback to be executed whenever event is published on provided keys

        Returns:
            object that can be used to cancel the subscription
        """
        keys = list(map(lambda k: EventKey.from_str(k), eventKeys))
        subscription = self.eventSubscriber.subscribe(keys, callback)
        # subscription.ready().await()
        return subscription

# XXX TODO
#     /**
#      * Subscribes to the given `eventKeys` and will execute the given `callback` on tick of specified `duration` with the latest event available.
#      * Throws [[csw.event.api.exceptions.EventServerNotAvailable]] when event server is not available.
#      *
#      * @param eventKeys collection of strings representing [[csw.params.events.EventKey]]
#      * @param duration which determines the frequency with which events are received
#      * @param callback to be executed whenever event is published on provided keys
#      * @return handle of [[esw.ocs.dsl.highlevel.models.EventSubscription]] which can be used to cancel the subscription
#      */
#     suspend fun onEvent(vararg eventKeys: String, duration: Duration, callback: SuspendableConsumer<Event>): EventSubscription {
#         cb = { event: Event -> coroutineScope.future { callback(event) } }
#         subscription = eventSubscriber
#                 .subscribeAsync(eventKeys.toEventKeys(), cb, duration.toJavaDuration(), SubscriptionModes.jRateAdapterMode())
#         subscription.ready().await()
#         return EventSubscription { subscription.unsubscribe().await() }
#     }
#
#     /**
#      * Method to get the latest event of all the provided `eventKeys`. Invalid event will be given if no event is published on one or more keys.
#      * Throws [[csw.event.api.exceptions.EventServerNotAvailable]] when event server is not available.
#      *
#      * @param eventKeys collection of strings representing [[csw.params.events.EventKey]].
#      * @return a [[kotlin.collections.Set]] of [[csw.params.events.Event]]
#      */
#     suspend fun getEvent(vararg eventKeys: String): Set<Event> =
#             eventSubscriber.get(eventKeys.toEventKeys()).await().toSet()
#
#     /**
#      * Method to get the latest event the provided `eventKey`. Invalid event will be given if no event is published on the key.
#      * Throws [[csw.event.api.exceptions.EventServerNotAvailable]] when event server is not available.
#      *
#      * @param eventKey strings representing [[csw.params.events.EventKey]].
#      * @return latest [[csw.params.events.Event]] available
#      */
#     suspend fun getEvent(eventKey: String): Event = eventSubscriber.get(EventKey(eventKey)).await()
#
#     private fun (Array<out String>).toEventKeys(): Set<EventKey> = map { EventKey.apply(it) }.toSet()
#
# }
