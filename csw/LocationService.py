from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import Enum
from multipledispatch import dispatch
import requests
import json

# Ignore generated functions in API docs
__pdoc__ = {}
def _pdocIgnoreGenerated(className: str):
    __pdoc__[f"{className}.from_dict"] = False
    __pdoc__[f"{className}.from_json"] = False
    __pdoc__[f"{className}.schema"] = False
    __pdoc__[f"{className}.to_dict"] = False
    __pdoc__[f"{className}.to_json"] = False


# Python API for CSW Location Service

class ComponentType(Enum):
    """
    Enum type: Represents a type of the CSW Component.
    """
    Assembly = "assembly"
    HCD = "hcd"
    Container = "container"
    Service = "service"
    Sequencer = "sequencer"


class ConnectionType(Enum):
    """
    Enum type: Represents a type of connection offered by the Component.
    Note that AkkaType is for Akka Actor based connections.
    Python applications can only communicate via HTTP or TCP connections.
    """
    HttpType = "http"
    TcpType = "tcp"
    AkkaType = "akka"


_pdocIgnoreGenerated("ConnectionInfo")
@dataclass_json
@dataclass
class ConnectionInfo:
    prefix: str
    componentType: str
    connectionType: str


_pdocIgnoreGenerated("ResolveInfo")
@dataclass_json
@dataclass
class ResolveInfo:
    _type: str
    connection: ConnectionInfo
    within: str

_pdocIgnoreGenerated("Location")
@dataclass_json
@dataclass
class Location:
    _type: str
    connection: ConnectionInfo
    uri: str
    metadata: dict

    @staticmethod
    def _makeLocation(obj: dict):
        typ = obj["_type"]
        s = json.dumps(obj)
        if typ == "HttpLocation":
            return HttpLocation.schema().loads(s)
        elif typ == "TcpLocation":
            return TcpLocation.schema().loads(s)
        elif typ == "AkkaLocation":
            return AkkaLocation.schema().loads(s)
        else:
            raise Exception("Invalid location type: " + typ)


_pdocIgnoreGenerated("AkkaLocation")
@dataclass_json
@dataclass
class AkkaLocation(Location):
    pass


_pdocIgnoreGenerated("TcpLocation")
@dataclass_json
@dataclass
class TcpLocation(Location):
    pass


_pdocIgnoreGenerated("HttpLocation")
@dataclass_json
@dataclass
class HttpLocation(Location):
    pass


_pdocIgnoreGenerated("Registration")
@dataclass_json
@dataclass
class Registration:
    """
    Abstract base class for registering with the location service
    """
    connection: ConnectionInfo
    port: int


_pdocIgnoreGenerated("NetworkType")
@dataclass_json
@dataclass
class NetworkType:
    """
    NetworkType enum {Outside, Inside)
    """
    _type: str

_pdocIgnoreGenerated("HttpRegistration")
@dataclass_json
@dataclass
class HttpRegistration(Registration):
    """
    Used to register an http based service with the Location Service.
    """
    path: str = ""
    networkType: NetworkType = NetworkType("Inside")
    metadata: dict = field(default_factory=dict)


_pdocIgnoreGenerated("TcpRegistration")
@dataclass_json
@dataclass
class TcpRegistration(Registration):
    """
    Used to register a tcp based service with the Location Service.
    """
    metadata: dict = field(default_factory=dict)


class LocationService:
    baseUri = "http://127.0.0.1:7654/"
    postUri = f"{baseUri}post-endpoint"
    wsUri = f"{baseUri}websocket-endpoint"

    # {"_type":"Register","registration":{"_type":"AkkaRegistration","connection":{"prefix":"CSW.testakkaservice_1","componentType":"service","connectionType":"akka"},"actorRefURI":"akka://TestAkkaServiceApp@192.168.178.32:40221/user/TestAkkaService1#1774679661"}}
    #
    def register(self, registration: Registration) -> ConnectionInfo:
        """
        Registers a connection.

        Args:
            registration (Registration): the Registration holding the connection and it's corresponding location to register with LocationService

        Returns: ConnectionInfo
            an object describing the connection
        """
        regType = registration.__class__.__name__
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
        print(f"Unregistering connection {connection} from the Location Service.")
        jsonBody = f'{{"_type": "Unregister", "connection": {connection.to_json()}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)

    def find(self, connection: ConnectionInfo) -> Location:
        """
        Resolves the location for a connection from the local cache

        Args:
            connection (ConnectionInfo): an already registered connection

        Returns: Location
            the Location
        """
        jsonBody = f'{{"_type": "Find", "connection": {connection.to_json()}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            return Location._makeLocation(maybeResult[0])

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
        jsonBody = resolveInfo.to_json()
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            return Location._makeLocation(maybeResult[0])

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

    def listByPrefix(self, prefix: str) -> List[Location]:
        """
        Lists all locations with the given prefix

        Args:
            prefix (str): restrict result to this prefix

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByPrefix", "prefix": "{prefix}"}}'
        return self._list(jsonBody)
