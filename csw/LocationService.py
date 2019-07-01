from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from multipledispatch import dispatch
import requests
import json


# Python API for CSW Location Service

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
    # Akka registration not supported in Python
    # AkkaRegistration = "AkkaRegistration"


@dataclass_json
@dataclass
class ConnectionInfo:
    name: str
    componentType: str
    connectionType: str


@dataclass_json
@dataclass
class Location:
    connection: ConnectionInfo
    uri: str

    @staticmethod
    def makeLocation(x: dict):
        # TODO: Handle AkkaLocation
        data = json.dumps(list(x.values())[0])
        key = list(x.keys())[0]
        if key == "HttpLocation":
            return HttpLocation.schema().loads(data)
        elif key == "TcpLocation":
            return TcpLocation.schema().loads(data)
        elif key == "AkkaLocation":
            return AkkaLocation.schema().loads(data)
        else:
            raise Exception("Invalid Location type: " + key)


@dataclass_json
@dataclass
class AkkaLocation(Location):
    prefix: str
    actorRef: str


@dataclass_json
@dataclass
class TcpLocation(Location):
    pass


@dataclass_json
@dataclass
class HttpLocation(Location):
    pass


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
        :param regType: the type of service being reisgtered
        :param registration: the Registration holding the connection and it's corresponding
                location to register with LocationService
        :return:
        """
        jsonBody = '{"' + regType.value + '": ' + registration.to_json() + '}'
        uri = self.baseUri + "register"
        r = requests.post(uri, json=json.loads(jsonBody))
        if not r.ok:
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
        if not r.ok:
            raise Exception(r.text)

    def find(self, name: str, componentType: ComponentType, connectionType: ConnectionType):
        """
        Resolves the location for a connection from the local cache
        :param name: name of the component or service
        :param componentType: type of the component or service
        :param connectionType: the type of connection
        :return: the Location
        """
        connectionName = f"{name}-{componentType.value}-{connectionType.value}"
        uri = f"{self.baseUri}find/{connectionName}"
        r = requests.get(uri)
        if not r.ok:
            raise Exception(r.text)
        return Location.makeLocation(json.loads(r.text))

    def resolve(self, name: str, componentType: ComponentType, connectionType: ConnectionType, withinSecs: str = "5"):
        """
        Resolves the location for a connection from the local cache, if not found waits for the event to arrive
        within specified time limit

        :param name: name of the component or service
        :param componentType: type of the component or service
        :param connectionType: the type of connection
        :param within: max number of seconds to wait for the connection to be found
        :return: the Location
        """
        connectionName = f"{name}-{componentType.value}-{connectionType.value}"
        uri = f"{self.baseUri}resolve/{connectionName}?within={withinSecs}s"
        r = requests.get(uri)
        if (not r.ok):
            raise Exception(r.text)
        return Location.makeLocation(json.loads(r.text))

    # def track(self, name: str, componentType: ComponentType, connectionType: ConnectionType, callback):
    #     """
    #     Tracks (monitors) the given connection and calls the given function whenever the connection state changes
    #
    #     :param name: name of the component or service
    #     :param componentType: type of the component or service
    #     :param connectionType: the type of connection
    #     :param callback: function to call when connection state changes
    #     """
    #     connectionName = f"{name}-{componentType.value}-{connectionType.value}"
    #     uri = f"{self.baseUri}resolve/{connectionName}"
    #     r = requests.get(uri)
    #     if (not r.ok):
    #         raise Exception(r.text)
    #     # TODO: handle receiving SSE and calling callback function


    def _list(self, uri: str):
        r = requests.get(uri)
        if (not r.ok):
            raise Exception(r.text)
        return list(map(lambda x: Location.makeLocation(x), json.loads(r.text)))

    @dispatch()
    def list(self):
        """
        Lists all locations registered
        :return: list of locations
        """
        uri = self.baseUri + "list"
        return self._list(uri)

    @dispatch(ComponentType)
    def list(self, componentType: ComponentType):
        """
        Lists components of the given component type
        :return: list of locations
        """
        uri = self.baseUri + "list?componentType=" + componentType.value
        return self._list(uri)

    @dispatch(str)
    def list(self, hostname: str):
        """
        Lists all locations registered on the given hostname
        :return: list of locations
        """
        uri = self.baseUri + "list?hostname=" + hostname
        return self._list(uri)

    @dispatch(ConnectionType)
    def list(self, connectionType: ConnectionType):
        """
        Lists all locations registered with the given connection type
        :return: list of locations
        """
        uri = self.baseUri + "list?connectionType=" + connectionType.value
        return self._list(uri)

    def listByPrefix(self, prefix: str):
        """
        Lists all locations with the given prefix
        :return: list of locations
        """
        uri = self.baseUri + "list?prefix=" + prefix
        return self._list(uri)

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
