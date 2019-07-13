from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from multipledispatch import dispatch
import requests
import json

# Python API for CSW Location Service
from openpyxl.pivot.table import Location


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
    def makeLocation(obj: dict) -> Location:
        data = json.dumps(list(obj.values())[0])
        key = list(obj.keys())[0]
        print(f"XXXXXXX makeLocation: obj = {str(obj)}, data = {str(data)}, key = {str(key)}")
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
    baseUri = "http://127.0.0.1:7654/location/"

    def register(self, regType: RegType, registration: Registration) -> ConnectionInfo:
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

    def find(self, name: str, componentType: ComponentType, connectionType: ConnectionType) -> Location:
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

    def resolve(self, name: str, componentType: ComponentType, connectionType: ConnectionType,
                withinSecs: str = "5") -> Location:
        """
        Resolves the location for a connection from the local cache, if not found waits for the event to arrive
        within specified time limit

        :param name: name of the component or service
        :param componentType: type of the component or service
        :param connectionType: the type of connection
        :param withinSecs: max number of seconds to wait for the connection to be found
        :return: the Location
        """
        connectionName = f"{name}-{componentType.value}-{connectionType.value}"
        uri = f"{self.baseUri}resolve/{connectionName}?within={withinSecs}s"
        r = requests.get(uri)
        if not r.ok:
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

    @staticmethod
    def _list(uri: str) -> List[Location]:
        r = requests.get(uri)
        if not r.ok:
            raise Exception(r.text)
        return list(map(lambda x: Location.makeLocation(x), json.loads(r.text)))

    @dispatch()
    def list(self) -> List[Location]:
        """
        Lists all locations registered
        :return: list of locations
        """
        uri = self.baseUri + "list"
        return self._list(uri)

    @dispatch(ComponentType)
    def list(self, componentType: ComponentType) -> List[Location]:
        """
        Lists components of the given component type
        :return: list of locations
        """
        uri = self.baseUri + "list?componentType=" + componentType.value
        return self._list(uri)

    @dispatch(str)
    def list(self, hostname: str) -> List[Location]:
        """
        Lists all locations registered on the given hostname
        :return: list of locations
        """
        uri = self.baseUri + "list?hostname=" + hostname
        return self._list(uri)

    @dispatch(ConnectionType)
    def list(self, connectionType: ConnectionType) -> List[Location]:
        """
        Lists all locations registered with the given connection type
        :return: list of locations
        """
        uri = self.baseUri + "list?connectionType=" + connectionType.value
        return self._list(uri)

    def listByPrefix(self, prefix: str) -> List[Location]:
        """
        Lists all locations with the given prefix
        :return: list of locations
        """
        uri = self.baseUri + "list?prefix=" + prefix
        return self._list(uri)
