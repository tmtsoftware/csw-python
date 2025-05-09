from collections.abc import Awaitable
from typing import List, Callable, Self
from dataclasses import dataclass, field
from socket import socket
import structlog
from aiohttp import ClientSession
from dataclasses_json import dataclass_json
from enum import Enum
from multipledispatch import dispatch
import json
from csw.Prefix import Prefix


def csw_version():
    return {"csw-version": "6.0.0"}


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
    Note that PekkoType is for Pekko Actor based connections.
    Python applications can only communicate via HTTP or TCP connections.
    """
    HttpType = "http"
    TcpType = "tcp"
    PekkoType = "pekko"


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


# noinspection PyUnresolvedReferences
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
            case "PekkoLocation":
                return PekkoLocation.from_dict(obj)
            case _:
                raise Exception(f"Invalid location type: {obj['_type']}")


@dataclass_json
@dataclass
class PekkoLocation(Location):
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
    networkType: NetworkType = field(default_factory=lambda: NetworkType("Inside"))
    metadata: dict = field(default_factory=csw_version)
    _type: str = "HttpRegistration"


@dataclass_json
@dataclass
class PekkoRegistration(Registration):
    """
    Used to register an http based service with the Location Service.
    """
    actorRefURI: str
    metadata: dict = field(default_factory=dict)
    _type: str = "PekkoRegistration"


@dataclass_json
@dataclass
class TcpRegistration(Registration):
    """
    Used to register a tcp based service with the Location Service.
    """
    port: int
    metadata: dict = field(default_factory=dict)
    _type: str = "TcpRegistration"


@dataclass
class RegistrationResult:
    unregister: Callable
    location: Location

    @classmethod
    def make(cls, _location: Location, _unregister: Callable[[ConnectionInfo], Awaitable]) -> Self:
        return cls(lambda: _unregister(_location.connection), _location)

class LocationServiceUtil:
    # If port is 0, return a random free port, otherwise the given port
    @staticmethod
    def getFreePort(port: int = 0) -> int:
        if port != 0:
            return port
        with socket() as s:
            s.bind(('', 0))
            return s.getsockname()[1]


# noinspection PyProtectedMember
class LocationService:
    log = structlog.get_logger()
    baseUri = "http://127.0.0.1:7654/"
    postUri = f"{baseUri}post-endpoint"

    def __init__(self, clientSession: ClientSession):
        self._session = clientSession

    async def register(self, registration: Registration) -> RegistrationResult:
        """
        Registers a connection.

        Args:
            registration (Registration): the Registration holding the connection and it's corresponding location to
            register with LocationService

        Returns: ConnectionInfo
            an object describing the connection
        """
        # noinspection PyUnresolvedReferences
        regJson = json.loads(registration.to_json())
        regJson['_type'] = registration.__class__.__name__
        jsonBody = f'{{"_type": "Register", "registration": {json.dumps(regJson)}}}'
        r = await self._session.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(await r.text())
        if len(maybeResult) != 0:
            location = Location._makeLocation(maybeResult)
            return RegistrationResult.make(location, self.unregister)

    async def unregister(self, connection: ConnectionInfo):
        """
        Unregisters a connection.

        Args:
            connection (ConnectionInfo): an already registered connection
        """
        self.log.debug(f"Unregistering connection {connection} from the Location Service.")
        # noinspection PyUnresolvedReferences
        jsonBody = f'{{"_type": "Unregister", "connection": {connection.to_json()}}}'
        r = await self._session.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(await r.text())

    async def _postJson(self, jsonBody: str) -> Location:
        r = await self._session.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(await r.text())
        if len(maybeResult) != 0:
            return Location._makeLocation(maybeResult[0])

    async def find(self, connection: ConnectionInfo) -> Location:
        """
        Resolves the location for a connection from the local cache

        Args:
            connection (ConnectionInfo): an already registered connection

        Returns: Location
            the Location
        """
        # noinspection PyUnresolvedReferences
        return await self._postJson(f'{{"_type": "Find", "connection": {connection.to_json()}}}')

    # "within":"2 seconds"}}
    async def resolve(self, connection: ConnectionInfo, withinSecs: int = "5") -> Location:
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
        # noinspection PyUnresolvedReferences
        return await self._postJson(resolveInfo.to_json())

    async def _list(self, jsonBody: str) -> List[Location]:
        r = await self._session.post(LocationService.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        return list(map(lambda x: Location._makeLocation(x), json.loads(await r.text())))

    @dispatch()
    async def list(self) -> List[Location]:
        """
        Lists all locations registered.

        Returns: List[Location]
            list of locations
        """
        jsonBody = '{"_type": "ListEntries"}'
        return await self._list(jsonBody)

    @dispatch(ComponentType)
    async def list(self, componentType: ComponentType) -> List[Location]:
        """
        Lists components of the given component type

        Args:
            componentType (ComponentType): the type of component to list

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByComponentType", "componentType": "{componentType.value}"}}'
        return await self._list(jsonBody)

    @dispatch(str)
    async def list(self, hostname: str) -> List[Location]:
        """
        Lists all locations registered on the given hostname

        Args:
            hostname (str): restrict result to this host

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByHostname", "hostname": "{hostname}"}}'
        return await self._list(jsonBody)

    @dispatch(ConnectionType)
    async def list(self, connectionType: ConnectionType) -> List[Location]:
        """
        Lists all locations registered with the given connection type

        Args:
            connectionType (ConnectionType): restrict result to this connection type

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByConnectionType", "connectionType": "{connectionType.value}"}}'
        return await self._list(jsonBody)

    async def listByPrefix(self, prefix: str) -> List[Location]:
        """
        Lists all locations with the given prefix

        Args:
            prefix (str): restrict result to those starting with prefix

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByPrefix", "prefix": "{prefix}"}}'
        return await self._list(jsonBody)

