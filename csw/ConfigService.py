from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List
from urllib.parse import urlencode

import re
from aiohttp import ClientSession
from dataclasses_json import dataclass_json
from keycloak import KeycloakOpenID

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from csw.Subsystem import Subsystem

@dataclass
class ConfigData:
    """
    Represents the contents of a file in the Config Service.
    You can get the content as a string with `s = configData.content.decode('utf-8')`.
    Create from a string with `ConfigData(bytes('hello', 'utf-8'))`.
    """
    content: bytes

    def __str__(self):
        return self.content.decode('utf-8')

@dataclass_json
@dataclass
class ConfigId:
    """
    Type of an id returned from ConfigManager create or update methods
    """
    id: str


@dataclass_json
@dataclass
class ConfigFileInfo:
    """
    Contains information about a config file stored in the config service
    """
    path: str
    id: str
    author: str
    comment: str


class FileType(Enum):
    """
    Represents the type of storage for a configuration file
    """
    Normal = 0
    Annex = 1


@dataclass_json
@dataclass
class ConfigMetadata:
    """
    Holds metadata information about config server
    """
    repoPath: str
    annexPath: str
    annexMinFileSize: str
    maxConfigFileSize: str


@dataclass_json
@dataclass
class ConfigFileRevision:
    """
    Holds information about a specific version of a config file
    """
    id: str
    author: str
    comment: str
    time: str


class ConfigService:

    def __init__(self,
                 clientSession: ClientSession,
                 client_id: str = "tmt-frontend-app",
                 user: str = "config-admin1",
                 password: str = "config-admin1",):
        self._session = clientSession
        self.client_id = client_id
        self.user = user
        self.password = password
        self._locationService = LocationService(clientSession)

    @staticmethod
    def _formatTime(time: datetime):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ")

    async def _getBaseUri(self) -> str:
        prefix = Prefix(Subsystem.CSW, "ConfigServer")
        connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
        location = await self._locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError("Can't locate CSW Config Service")

    async def _endPoint(self, path: str) -> str:
        return f'{await self._getBaseUri()}{path}'

    async def _locateAuthService(self) -> str:
        connection = ConnectionInfo.make(Prefix(Subsystem.CSW, "AAS"), ComponentType.Service, ConnectionType.HttpType)
        location = await self._locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError("Can't locate CSW Auth Service")

    async def _getToken(self):
        uri = await self._locateAuthService()
        keycloak_openid = KeycloakOpenID(server_url=f'{uri}/',
                                         client_id=self.client_id,
                                         realm_name='TMT')
        d = keycloak_openid.token(self.user, self.password)
        return d['access_token']

    @staticmethod
    def _validatePath(path: str):
        invalidChars = "!#<>$%&'@^`~+,;=\\s"
        if re.match(invalidChars, path):
            charsMessage = invalidChars.replace('\\s', '')
            raise RuntimeError(
                f"Input file path '{path}' contains invalid characters. "
                + f"Note, these characters {charsMessage} or 'white space' are not allowed in file path`")

    async def _createOrUpdate(self, create: bool, path: str, configData: ConfigData,
                        annex: bool = False, comment: str = "Created") -> ConfigId:
        self._validatePath(path)
        token = await self._getToken()
        params = urlencode({'annex': annex, 'comment': comment})
        baseUri = await self._endPoint(f'config/{path}')
        uri = f'{baseUri}?{params}'
        headers = {'Content-type': 'application/octet-stream', 'Authorization': f'Bearer {token}'}
        if create:
            response = await self._session.post(uri, headers=headers, data=configData.content)
        else:
            response = await self._session.put(uri, headers=headers, data=configData.content)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigId(await response.json())

    async def create(self, path: str, configData: ConfigData, annex: bool = False, comment: str = "Created") -> ConfigId:
        """
        Creates a file at a specified path with given data and comment.

        Args:
            path (str): the file path relative to the repository root
            configData (ConfigData): contents of the file
            annex (bool): true if the file is annex and requires special handling (external storage)
            comment (str): comment to associate with this operation

        Returns: id of file revision
        """
        return await self._createOrUpdate(True, path, configData, annex, comment)

    async def update(self, path: str, configData: ConfigData, annex: bool = False, comment: str = "Created") -> ConfigId:
        """
        Updates a file at a specified path with given data and comment.

        Args:
            path (str): the file path relative to the repository root
            configData (ConfigData): contents of the file
            annex (bool): true if the file is annex and requires special handling (external storage)
            comment (str): comment to associate with this operation

        Returns: id of file revision
        """
        return await self._createOrUpdate(False, path, configData, annex, comment)

    async def delete(self, path: str, comment: str = "Deleted"):
        """
        Deletes the given config file (older versions will still be available).

        Args:
            path: the file path relative to the repository root
            comment: comment to associate with this operation
        """
        token = await self._getToken()
        params = urlencode({'comment': comment})
        baseUri = await self._endPoint(f'config/{path}')
        uri = f'{baseUri}?{params}'
        headers = {'Authorization': f'Bearer {token}'}
        response = await self._session.delete(uri, headers=headers)
        if not response.ok:
            raise RuntimeError(await response.text())

    # noinspection PyUnresolvedReferences
    async def list(self, fileType: FileType = None, pattern: str = None) -> List[ConfigFileInfo]:
        """
        Returns a list containing all the known config files of given type(Annex or Normal) and whose name matches the provided pattern.

        Args:
            fileType: optional file type(Annex or Normal)
            pattern: optional pattern to match against the file name

        Returns: list of ConfigFileInfo

        """
        params = {}
        if fileType:
            params.update({'type': fileType.name})
        if pattern:
            params.update({'pattern': pattern})
        uri = f"{await self._endPoint('list')}?{urlencode(params)}"
        response = await self._session.get(uri)
        return list(map(lambda p: ConfigFileInfo.from_dict(p), await response.json()))

    async def exists(self, path: str, configId: ConfigId = None):
        """
        Returns true if the given path exists and is being managed.

        Args:
            path: the file path relative to the repository root
            configId: revision of the file

        Returns: true if the file exists in the repo
        """
        params = {}
        if configId:
            params.update({'id': configId.id})
        uri = f"{await self._endPoint('config')}/{path}?{urlencode(params)}"
        response = await self._session.head(uri)
        return response.ok

    async def getLatest(self, path: str) -> ConfigData:
        """
        Gets and returns the content of latest version of the file stored under the given path.

        Args:
            path (str): the file path relative to the repository root

        Returns: file contents
        """
        uri = f"{await self._endPoint('config')}/{path}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigData(await response.content.read())

    async def getById(self, path: str, configId: ConfigId) -> ConfigData:
        """
        Gets and returns the file at the given path with the specified revision id

        Args:
            path (str): the file path relative to the repository root
            configId (ConfigId):  id used to specify a specific version to fetch

        Returns: file contents
        """
        params = {'id': configId.id}
        uri = f"{await self._endPoint('config')}/{path}?{urlencode(params)}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigData(await response.content.read())

    async def getByTime(self, path: str, time: datetime) -> ConfigData:
        """
        Gets the file at the given path as it existed on the given instant.
        If instant is before the file was created, the initial version is returned.
        If instant is after the last change, the most recent version is returned.

        Args:
            path (str): the file path relative to the repository root
            time (datetime): the target instant

        Returns: file contents
        """
        params = {'date': self._formatTime(time)}
        uri = f"{await self._endPoint('config')}/{path}?{urlencode(params)}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigData(await response.content.read())

    async def getActive(self, path: str) -> ConfigData:
        """
        Gets and returns the content of active version of the file stored under the given path.

        Args:
            path (str): the file path relative to the repository root

        Returns: file contents

        """
        uri = f"{await self._endPoint('active-config')}/{path}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigData(await response.content.read())

    async def getActiveByTime(self, path: str, time: datetime) -> ConfigData:
        """
        Returns the content of active version of the file at the given path as it existed on the given instant

        Args:
            path (str): the file path relative to the repository root
            time (datetime): the target instant

        Returns: file contents

        """
        params = {'date': self._formatTime(time)}
        uri = f"{await self._endPoint('active-config')}/{path}?{urlencode(params)}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigData(await response.content.read())

    async def getActiveVersion(self, path: str) -> ConfigId:
        """
        Returns the version which represents the "active version" of the file at the given path.

        Args:
            path (str): the file path relative to the repository root

        Returns: ConfigId indicating the id of the active version

        """
        uri = f"{await self._endPoint('active-version')}/{path}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigId(await response.json())

    # noinspection PyUnresolvedReferences
    async def getMetadata(self) -> ConfigMetadata:
        """
        Query the metadata of config server.
        Returns: a ConfigMetadata object

        """
        uri = f"{await self._endPoint('metadata')}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return ConfigMetadata.from_dict(await response.json())

    # noinspection PyUnresolvedReferences
    async def _history(self, key: str, path: str,
                 fromTime: datetime, toTime: datetime,
                 maxResults: int) -> List[ConfigFileRevision]:
        params = {}
        if fromTime:
            params.update({'from': self._formatTime(fromTime)})
        if toTime:
            params.update({'to': self._formatTime(toTime)})
        if maxResults:
            params.update({'maxResults': maxResults})
        uri = f"{await self._endPoint(key)}/{path}?{urlencode(params)}"
        response = await self._session.get(uri)
        if not response.ok:
            raise RuntimeError(await response.text())
        return list(map(lambda p: ConfigFileRevision.from_dict(p), await response.json()))

    async def history(self, path: str,
                fromTime: datetime = None, toTime: datetime = None,
                maxResults: int = 10000) -> List[ConfigFileRevision]:
        """
        Returns the history of versions of the file at the given path for a range of period specified by from and to.
        The size of the list is limited up to maxResults.

        Args:
            path: the file path relative to the repository root
            fromTime: optional start of the history range
            toTime: optional end of the history range
            maxResults: optional maximum number of history results to return (default: unlimited)

        Returns: list of ConfigFileRevision

        """
        return await self._history('history', path, fromTime, toTime, maxResults)

    async def historyActive(self, path: str,
                      fromTime: datetime = None, toTime: datetime = None,
                      maxResults: int = None) -> List[ConfigFileRevision]:
        """
        Returns the history of active versions of the file at the given path for a range of period specified by
        fromTime and toTime. The size of the list is limited upto maxResults.

        Args:
            path: the file path relative to the repository root
            fromTime: optional start of the history range
            toTime: optional end of the history range
            maxResults: optional maximum number of history results to return (default: unlimited)

        Returns: list of ConfigFileRevision

        """
        return await self._history('history-active', path, fromTime, toTime, maxResults)

    async def setActiveVersion(self, path: str, configId: ConfigId, comment: str):
        """
        Sets the active version to be the version provided for the file at the given path.
        If this method is not called, the active version will always be the version with which the file was created.
        After calling this method, the version with the given Id will be the active version.

        Args:
            path: the file path relative to the repository root
            configId: an id used to specify a specific version (by default the id of the version with which
                      the file was created i.e. 1)
            comment: comment to associate with this operation

        """
        token = await self._getToken()
        params = {'id': configId.id, 'comment': comment}
        headers = {'Authorization': f'Bearer {token}'}
        uri = f"{await self._endPoint('active-version')}/{path}?{urlencode(params)}"
        response = await self._session.put(uri, headers=headers)
        if not response.ok:
            raise RuntimeError(await response.text())

    async def resetActiveVersion(self, path: str, comment: str):
        """
        Resets the "active version" of the file at the given path to the latest version.

        Args:
            path: the file path relative to the repository root
            comment: comment to associate with this operation

        """
        token = await self._getToken()
        params = {'comment': comment}
        headers = {'Authorization': f'Bearer {token}'}
        uri = f"{await self._endPoint('active-version')}/{path}?{urlencode(params)}"
        response = await self._session.put(uri, headers=headers)
        if not response.ok:
            raise RuntimeError(await response.text())
