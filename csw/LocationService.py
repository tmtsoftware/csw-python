from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
import requests
import json


class ComponentType(Enum):
    Assembly = "assembly"
    HCD = "hcd"
    Container = "container"
    Service = "service"
    Sequencer = "sequencer"


class ConnectionType(Enum):
    HttpType = "http"
    TcpType = "tcp"
    AkkaType = "akka"


class RegType(Enum):
    HttpRegistration = "HttpRegistration"
    TcpRegistration = "TcpRegistration"
    # AkkaRegistration = "AkkaRegistration"


@dataclass_json
@dataclass
class ConnectionInfo:
    name: str
    componentType: str
    connectionType: str


@dataclass_json
@dataclass
class AkkaLocation:
    # type: str
    connection: ConnectionInfo
    uri: str
    prefix: str
    actorRef: any


@dataclass_json
@dataclass
class TcpLocation:
    # type: str
    connection: ConnectionInfo
    uri: str


@dataclass_json
@dataclass
class HttpLocation:
    # type: str
    connection: ConnectionInfo
    uri: str


class Location:

    @staticmethod
    def makeLocation(x: dict):
        # TODO: Handle AkkaLocation
        data = json.dumps(list(x.values())[0])
        key = list(x.keys())[0]
        if (key == "HttpLocation"):
            return HttpLocation.schema().loads(data)
        elif (key == "TcpLocation"):
            return TcpLocation.schema().loads(data)
        elif (key == "AkkaLocation"):
            return AkkaLocation.schema().loads(data)
        else:
            raise Exception("Invalid Location type: " + key)


@dataclass_json
@dataclass
class Registration:
    """
    Used to register with the Location Service.
    """
    port: int
    connection: ConnectionInfo
    path: str = ""


class LocationService:
    baseUri = uri = "http://127.0.0.1:7654/location/"

    def register(self, regType: RegType, registration: Registration):
        """
        Registers a connection.
        :param registration: the Registration holding connection and it's corresponding location to register with LocationService
        :return:
        """
        jsonBody = '{"' + regType.value + '": ' + registration.to_json() + '}'
        uri = self.baseUri + "register"
        r = requests.post(uri, json=json.loads(jsonBody))
        if (not r.ok):
            raise Exception(r.text)
        return registration.connection

    def unregister(self, connection: ConnectionInfo):
        """
        Unregisters a connection.
        :param connection: an already registered connection
        :return:
        """
        jsonBody = connection.to_json()
        uri = self.baseUri + "unregister"
        r = requests.post(uri, json=json.loads(jsonBody))
        if (not r.ok):
            raise Exception(r.text)

    def list(self):
        uri = self.baseUri + "list"
        r = requests.get(uri)
        if (not r.ok):
            raise Exception(r.text)
        return list(map(lambda x: Location.makeLocation(x), json.loads(r.text)))

    # /**
    # * Registers a connection -> location in cluster
    # *
    # * @param registration the Registration holding connection and it's corresponding location to register with `LocationService`
    # * @return a future which completes with Registration result or can fail with
    # *         [[csw.location.api.exceptions.RegistrationFailed]] or [[csw.location.api.exceptions.OtherLocationIsRegistered]]
    # */
    # def register(registration: Registration): Future[RegistrationResult]
    #
    # /**
    # * Unregisters the connection
    # *
    # * @note this method is idempotent, which means multiple call to unregister the same connection will be no-op once successfully
    # *       unregistered from location service
    # * @param connection an already registered connection
    # * @return a future which completes after un-registration happens successfully and fails otherwise with
    #     *         [[csw.location.api.exceptions.UnregistrationFailed]]
    # */
    # def unregister(connection: Connection): Future[Done]
    #
    # /**
    # * Unregisters all connections
    # *
    # * @note it is highly recommended to use this method for testing purpose only
    # * @return a future which completes after all connections are unregistered successfully or fails otherwise with
    #     *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def unregisterAll(): Future[Done]
    #
    # /**
    # * Resolves the location for a connection from the local cache
    # *
    # * @param connection a connection to resolve to with its registered location
    # * @return a future which completes with the resolved location if found or None otherwise. It can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]].
    # */
    # def find[L <: Location](connection: TypedConnection[L]): Future[Option[L]]
    #
    # /**
    # * Resolves the location for a connection from the local cache, if not found waits for the event to arrive
    # * within specified time limit. Returns None if both fail.
    # *
    # * @param connection a connection to resolve to with its registered location
    # * @param within max wait time for event to arrive
    # * @tparam L the concrete Location type returned once the connection is resolved
    # * @return a future which completes with the resolved location if found or None otherwise. It can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]].
    # */
    # def resolve[L <: Location](connection: TypedConnection[L], within: FiniteDuration): Future[Option[L]]
    #
    # /**
    # * Lists all locations registered
    # *
    # * @return a future which completes with a List of all registered locations or can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def list: Future[List[Location]]
    #
    # /**
    # * Filters all locations registered based on a component type
    # *
    # * @param componentType list components of this `componentType`
    # * @return a future which completes with filtered locations or can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def list(componentType: ComponentType): Future[List[Location]]
    #
    # /**
    # * Filters all locations registered based on a hostname
    # *
    # * @param hostname list components running on this `hostname`
    # * @return a future which completes with filtered locations or can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def list(hostname: String): Future[List[Location]]
    #
    # /**
    # * Filters all locations registered based on a connection type
    # *
    # * @param connectionType list components of this `connectionType`
    # * @return a future which completes with filtered locations or can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def list(connectionType: ConnectionType): Future[List[Location]]
    #
    # /**
    # * Filters all locations registered based on a prefix.
    # *
    # * @note all locations having subsystem prefix that starts with the given prefix
    # *       value will be listed.
    # * @param prefix list components by this `prefix`
    # * @return a future which completes with filtered locations or can fail with
    # *         [[csw.location.api.exceptions.RegistrationListingFailed]]
    # */
    # def listByPrefix(prefix: String): Future[List[AkkaLocation]]
    #
    # /**
    # * Tracks the connection and send events for modification or removal of its location
    # *
    # * @param connection the `connection` that is to be tracked
    # * @return A stream that emits events related to the connection. It can be cancelled using KillSwitch. This will stop giving
    # *         events for earlier tracked connection
    # */
    # def track(connection: Connection): Source[TrackingEvent, KillSwitch]
    #
    # /**
    # * Subscribe to tracking events for a connection by providing a callback
    # * For each event the callback is invoked.
    # * Use this method if you do not want to handle materialization and happy with a side-effecting callback instead.
    # *
    # * @note Callbacks are not thread-safe on the JVM. If you are doing side effects/mutations inside the callback, you should ensure that it is done in a thread-safe way inside an actor.
    # * @param connection the `connection` that is to be tracked
    # * @param callback the callback function of type `TrackingEvent` => Unit which gets executed on receiving any `TrackingEvent`
    # * @return a killswitch which can be shutdown to unsubscribe the consumer
    # */
    # def subscribe(connection: Connection, callback: TrackingEvent ⇒ Unit): KillSwitch
