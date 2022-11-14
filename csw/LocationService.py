from typing import List
from dataclasses import dataclass, field
from socket import socket
import structlog
from dataclasses_json import dataclass_json
from enum import Enum
from multipledispatch import dispatch
import requests
import json
from csw.Prefix import Prefix


def csw_version():
    return {"csw-version": "5.0.0"}


# Python API for CSW Location Service

# TODO: Add Location Service subscribe / TrackingEvent

#  "ComponentType" : [ "Container", "HCD", "Assembly", "Sequencer", "SequenceComponent", "Service", "Machine" ],

class ComponentType(Enum):
    """
    Enum type: Represents a type of the CSW Component.
    """
    Assembly = "Assembly"
    HCD = "HCD"
    Container = "Container"
    Service = "Service"
    Sequencer = "Sequencer"
    SequenceComponent = "SequenceComponent"
    Machine = "Machine"


class ConnectionType(Enum):
    """
    Enum type: Represents a type of connection offered by the Component.
    Note that AkkaType is for Akka Actor based connections.
    Python applications can only communicate via HTTP or TCP connections.
    """
    HttpType = "http"
    TcpType = "tcp"
    AkkaType = "akka"


@dataclass_json
@dataclass
class ComponentId:
    prefix: str
    componentType: str


@dataclass_json
@dataclass
class ConnectionInfo:
    prefix: str
    componentType: str
    connectionType: str

    @staticmethod
    def make(prefix: Prefix, componentType: ComponentType, connectionType: ConnectionType):
        return ConnectionInfo(str(prefix), componentType.value, connectionType.value)


@dataclass_json
@dataclass
class ResolveInfo:
    _type: str
    connection: ConnectionInfo
    within: str


@dataclass_json
@dataclass
class Location:
    _type: str
    connection: ConnectionInfo
    uri: str
    metadata: dict

    @staticmethod
    def _makeLocation(obj: dict):
        match obj['_type']:
            case "HttpLocation":
                return HttpLocation.from_dict(obj)
            case "TcpLocation":
                return TcpLocation.from_dict(obj)
            case "AkkaLocation":
                return AkkaLocation.from_dict(obj)
            case _:
                raise Exception(f"Invalid location type: {obj['_type']}")


@dataclass_json
@dataclass
class AkkaLocation(Location):
    pass


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
    Abstract base class for registering with the location service
    """
    connection: ConnectionInfo


@dataclass_json
@dataclass
class NetworkType:
    """
    NetworkType enum {Outside, Inside)
    """
    _type: str


@dataclass_json
@dataclass
class HttpRegistration(Registration):
    """
    Used to register an http based service with the Location Service.
    """
    port: int
    path: str = ""
    networkType: NetworkType = NetworkType("Inside")
    metadata: dict = field(default_factory=csw_version)
    _type: str = "HttpRegistration"


@dataclass_json
@dataclass
class AkkaRegistration(Registration):
    """
    Used to register an http based service with the Location Service.
    """
    actorRefURI: str
    metadata: dict = field(default_factory=dict)
    _type: str = "AkkaRegistration"


@dataclass_json
@dataclass
class TcpRegistration(Registration):
    """
    Used to register a tcp based service with the Location Service.
    """
    port: int
    metadata: dict = field(default_factory=dict)
    _type: str = "TcpRegistration"


# noinspection PyProtectedMember
class LocationService:
    log = structlog.get_logger()
    baseUri = "http://127.0.0.1:7654/"
    postUri = f"{baseUri}post-endpoint"

    # If port is 0, return a random free port, otherwise the given port
    @staticmethod
    def getFreePort(port: int = 0) -> int:
        if port != 0:
            return port
        with socket() as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def register(self, registration: Registration) -> ConnectionInfo:
        """
        Registers a connection.

        Args:
            registration (Registration): the Registration holding the connection and it's corresponding location to
            register with LocationService

        Returns: ConnectionInfo
            an object describing the connection
        """
        # regType = registration.__class__.__name__
        regJson = json.loads(registration.to_json())
        regJson['_type'] = registration.__class__.__name__
        jsonBody = f'{{"_type": "Register", "registration": {json.dumps(regJson)}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        return registration.connection

    def unregister(self, connection: ConnectionInfo):
        """
        Unregisters a connection.

        Args:
            connection (ConnectionInfo): an already registered connection
        """
        self.log.debug(f"Unregistering connection {connection} from the Location Service.")
        jsonBody = f'{{"_type": "Unregister", "connection": {connection.to_json()}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)

    def _postJson(self, jsonBody: str) -> Location:
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            return Location._makeLocation(maybeResult[0])

    def find(self, connection: ConnectionInfo) -> Location:
        """
        Resolves the location for a connection from the local cache

        Args:
            connection (ConnectionInfo): an already registered connection

        Returns: Location
            the Location
        """
        return self._postJson(f'{{"_type": "Find", "connection": {connection.to_json()}}}')

    # "within":"2 seconds"}}
    def resolve(self, connection: ConnectionInfo, withinSecs: int = "5") -> Location:
        """
        Resolves the location for a connection from the local cache, if not found waits for the event to arrive
        within specified time limit

        Args:
            connection (ConnectionInfo): an already registered connection
            withinSecs (int): max number of seconds to wait for the connection to be found

        Returns: Location
            the Location
        """
        resolveInfo = ResolveInfo("Resolve", connection, f"{withinSecs} seconds")
        return self._postJson(resolveInfo.to_json())

    @staticmethod
    def _list(jsonBody: str) -> List[Location]:
        r = requests.post(LocationService.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        return list(map(lambda x: Location._makeLocation(x), json.loads(r.text)))

    @dispatch()
    def list(self) -> List[Location]:
        """
        Lists all locations registered.

        Returns: List[Location]
            list of locations
        """
        jsonBody = '{"_type": "ListEntries"}'
        return self._list(jsonBody)

    @dispatch(ComponentType)
    def list(self, componentType: ComponentType) -> List[Location]:
        """
        Lists components of the given component type

        Args:
            componentType (ComponentType): the type of component to list

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByComponentType", "componentType": "{componentType.value}"}}'
        return self._list(jsonBody)

    @dispatch(str)
    def list(self, hostname: str) -> List[Location]:
        """
        Lists all locations registered on the given hostname

        Args:
            hostname (str): restrict result to this host

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByHostname", "hostname": "{hostname}"}}'
        return self._list(jsonBody)

    @dispatch(ConnectionType)
    def list(self, connectionType: ConnectionType) -> List[Location]:
        """
        Lists all locations registered with the given connection type

        Args:
            connectionType (ConnectionType): restrict result to this connection type

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByConnectionType", "connectionType": "{connectionType.value}"}}'
        return self._list(jsonBody)

    def listByPrefix(self, prefix: Prefix) -> List[Location]:
        """
        Lists all locations with the given prefix

        Args:
            prefix (Prefix): restrict result to this prefix

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByPrefix", "prefix": "{str(prefix)}"}}'
        return self._list(jsonBody)

