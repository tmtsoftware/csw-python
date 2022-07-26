import json
from dataclasses import dataclass
from enum import Enum
from typing import List
from urllib.parse import urlencode

import requests
from dataclasses_json import dataclass_json
from keycloak import KeycloakOpenID

from csw.LocationService import LocationService, ConnectionInfo, ComponentType, ConnectionType, HttpLocation
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems


@dataclass
class ConfigData:
    content: bytes


@dataclass_json
@dataclass
class ConfigId:
    id: str


@dataclass_json
@dataclass
class ConfigFileInfo:
    path: str
    id: str
    author: str
    comment: str


class FileType(Enum):
    Normal = 0
    Annex = 1


class ConfigService:
    @staticmethod
    def _getBaseUri() -> str:
        prefix = Prefix(Subsystems.CSW, "ConfigServer")
        locationService = LocationService()
        connection = ConnectionInfo.make(prefix, ComponentType.Service, ConnectionType.HttpType)
        location = locationService.resolve(connection)
        if location is not None:
            location.__class__ = HttpLocation
            return location.uri
        raise RuntimeError

    def _endPoint(self, path: str) -> str:
        return f'{self._getBaseUri()}{path}'

    def _getToken(self):
        keycloak_openid = KeycloakOpenID(server_url='http://localhost:8081/auth/',
                                         client_id='tmt-frontend-app',
                                         realm_name='TMT')
        d = keycloak_openid.token("config-admin1", "config-admin1")
        return d['access_token']

    # XXX TODO FIXME not working
    def create(self, path: str, configData: ConfigData, annex: bool = False, comment: str = "Created") -> ConfigId:
        # ConfigUtils.validatePath(path)
        token = self._getToken()
        params = urlencode({'annex': annex, 'comment': comment})
        baseUri = self._endPoint(f'config/{path}')
        uri = f'{baseUri}?{params}'
        headers = {'Content-type': 'application/octet-stream', 'Authorization': f'Bearer {token}'}
        response = requests.post(uri, headers=headers, data=configData.content)
        if not response.ok:
            raise RuntimeError(response.text)
        return ConfigId(response.text)

    def list(self, fileType: FileType = None, pattern: str = None) -> List[ConfigFileInfo]:
        params = {}
        if fileType:
            params.update({'type': fileType.name})
        if pattern:
            params.update({'pattern': pattern})
        uri = f"{self._endPoint(f'list')}?{urlencode(params)}"
        response = requests.get(uri)
        return list(map(lambda p: ConfigFileInfo.from_dict(p), response.json()))


    def exists(self, path: str, configId: ConfigId = None):
        params = {}
        if configId:
            params.update({'id': configId.id})
        uri = f"{self._endPoint(f'config')}/{path}?{urlencode(params)}"
        response = requests.head(uri)
        return response.ok

    def getLatest(self, path: str) -> ConfigData:
        uri = f"{self._endPoint(f'config')}/{path}"
        response = requests.get(uri)
        if not response.ok:
            raise RuntimeError(response.text)
        return ConfigData(response.content)
