from typing import List
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

@dataclass_json
@dataclass
class ConnectionInfo:
    prefix: str
    componentType: str
    connectionType: str


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

    @staticmethod
    def makeLocation(obj: dict):
        typ = obj["_type"]
        s = json.dumps(obj)
        if typ == "HttpLocation":
            return HttpLocation.schema().loads(s)
        elif typ == "TcpLocation":
            return TcpLocation.schema().loads(s)
        elif typ == "AkkaLocation":
            return AkkaLocation.schema().loads(s)
        else:
            raise Exception("Invalid Location type: " + typ)


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
    port: int


@dataclass_json
@dataclass
class HttpRegistration(Registration):
    """
    Used to register an http based service with the Location Service.
    """
    path: str = ""


@dataclass_json
@dataclass
class TcpRegistration(Registration):
    """
    Used to register a tcp based service with the Location Service.
    """

class LocationService:
    baseUri = "http://127.0.0.1:7654/"
    postUri = f"{baseUri}post-endpoint"
    wsUri = f"{baseUri}websocket-endpoint"

    # {"_type":"Register","registration":{"_type":"AkkaRegistration","connection":{"prefix":"CSW.testakkaservice_1","componentType":"service","connectionType":"akka"},"actorRefURI":"akka://TestAkkaServiceApp@192.168.178.32:40221/user/TestAkkaService1#1774679661"}}
    #
    def register(self, registration: Registration) -> ConnectionInfo:
        """
        Registers a connection.
        :param registration: the Registration holding the connection and it's corresponding
                location to register with LocationService
        :return:
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
        :param connection: an already registered connection
        :return:
        """
        print(f"Unregistering connection {connection} from the Location Service.")
        jsonBody = f'{{"_type": "Unregister", "connection": {connection.to_json()}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)

    def find(self, connection: ConnectionInfo) -> Location:
        """
        Resolves the location for a connection from the local cache
        :param connection: an already registered connection
        :return: the Location
        """
        jsonBody = f'{{"_type": "Find", "connection": {connection.to_json()}}}'
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            return Location.makeLocation(maybeResult[0])

    # "within":"2 seconds"}}
    def resolve(self, connection: ConnectionInfo, withinSecs: int = "5") -> Location:
        """
        Resolves the location for a connection from the local cache, if not found waits for the event to arrive
        within specified time limit

        :param connection: an already registered connection
        :param withinSecs: max number of seconds to wait for the connection to be found
        :return: the Location
        """
        resolveInfo = ResolveInfo("Resolve", connection, f"{withinSecs} seconds")
        jsonBody = resolveInfo.to_json()
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            return Location.makeLocation(maybeResult[0])

    @staticmethod
    def _list(jsonBody: str) -> List[Location]:
        r = requests.post(LocationService.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        return list(map(lambda x: Location.makeLocation(x), json.loads(r.text)))

    @dispatch()
    def list(self) -> List[Location]:
        """
        Lists all locations registered
        :return: list of locations
        """
        jsonBody = '{"_type": "ListEntries"}'
        return self._list(jsonBody)

    @dispatch(ComponentType)
    def list(self, componentType: ComponentType) -> List[Location]:
        """
        Lists components of the given component type
        :return: list of locations
        """
        jsonBody = f'{{"_type": "ListByComponentType", "componentType": "{componentType.value}"}}'
        return self._list(jsonBody)

    @dispatch(str)
    def list(self, hostname: str) -> List[Location]:
        """
        Lists all locations registered on the given hostname
        :return: list of locations
        """
        jsonBody = f'{{"_type": "ListByHostname", "hostname": "{hostname}"}}'
        return self._list(jsonBody)

    @dispatch(ConnectionType)
    def list(self, connectionType: ConnectionType) -> List[Location]:
        """
        Lists all locations registered with the given connection type
        :return: list of locations
        """
        jsonBody = f'{{"_type": "ListByConnectionType", "connectionType": "{connectionType.value}"}}'
        return self._list(jsonBody)

    def listByPrefix(self, prefix: str) -> List[Location]:
        """
        Lists all locations with the given prefix
        :return: list of locations
        """
        jsonBody = f'{{"_type": "ListByPrefix", "prefix": "{prefix}"}}'
        return self._list(jsonBody)
