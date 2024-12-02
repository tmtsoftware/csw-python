from typing import List
import structlog
from multipledispatch import dispatch
import requests
import json

from csw.LocationService import Registration, RegistrationResult, Location, ConnectionInfo, ResolveInfo, ComponentType, \
    ConnectionType


# noinspection PyProtectedMember
class LocationServiceSync:
    """
    A version of Location Service that does not use async
    """

    log = structlog.get_logger()
    baseUri = "http://127.0.0.1:7654/"
    postUri = f"{baseUri}post-endpoint"

    def register(self, registration: Registration) -> RegistrationResult:
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
        r = requests.post(self.postUri, json=json.loads(jsonBody))
        if not r.ok:
            raise Exception(r.text)
        maybeResult = json.loads(r.text)
        if len(maybeResult) != 0:
            location = Location._makeLocation(maybeResult)
            return RegistrationResult.make(location, self.unregister)

    def unregister(self, connection: ConnectionInfo):
        """
        Unregisters a connection.

        Args:
            connection (ConnectionInfo): an already registered connection
        """
        self.log.debug(f"Unregistering connection {connection} from the Location Service.")
        # noinspection PyUnresolvedReferences
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
        # noinspection PyUnresolvedReferences
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
        # noinspection PyUnresolvedReferences
        return self._postJson(resolveInfo.to_json())

    def _list(self, jsonBody: str) -> List[Location]:
        r = requests.post(LocationServiceSync.postUri, json=json.loads(jsonBody))
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
            prefix (str): restrict result to those starting with prefix

        Returns: List[Location]
            list of locations
        """
        jsonBody = f'{{"_type": "ListByPrefix", "prefix": "{prefix}"}}'
        return self._list(jsonBody)
