import sys
import os
import time
import json

import structlog
from _pytest import pathlib

from csw.Subsystem import Subsystems
from csw.Prefix import Prefix
from csw.LocationService import ComponentType, ConnectionInfo, HttpRegistration, TcpRegistration, \
    AkkaRegistration, ComponentId, ConnectionType, AkkaLocation, HttpLocation, TcpLocation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCswContract:
    log = structlog.get_logger()

    # Validate against contract file produced by csw
    def test_location_service_models(self):
        dir = pathlib.Path(__file__).parent.absolute()
        with open(f"{dir}/location_models.json") as json_file:
            data = json.load(json_file)
            for p in data['ComponentType']:
                assert (ComponentType[p].value == p)
            for p in data['Connection']:
                connectionInfo = ConnectionInfo.from_dict(p)
                self.log.debug(f"Connection: {connectionInfo}")
                assert (connectionInfo.to_dict() == p)
            for p in data['Registration']:
                regType = p['_type']
                if (regType == "HttpRegistration"):
                    registration = HttpRegistration.from_dict(p)
                elif (regType == "TcpRegistration"):
                    registration = TcpRegistration.from_dict(p)
                elif (regType == "AkkaRegistration"):
                    registration = AkkaRegistration.from_dict(p)
                assert (registration.to_dict() == p)
            for p in data['ComponentId']:
                componentId = ComponentId.from_dict(p)
                self.log.debug(f"ComponentId: {componentId}")
                assert (componentId.to_dict() == p)
            for p in data['Prefix']:
                prefix = Prefix.from_str(p)
                assert (str(prefix) == p)
            for p in data['ConnectionType']:
                assert (ConnectionType(p).value == p)
            for p in data['Subsystem']:
                assert (Subsystems[p].name == p)
            for p in data['Location']:
                locType = p['_type']
                if (locType == "AkkaLocation"):
                    loc = AkkaLocation.from_dict(p)
                elif (locType == "HttpLocation"):
                    loc = HttpLocation.from_dict(p)
                elif (locType == "TcpLocation"):
                    loc = TcpLocation.from_dict(p)
                self.log.debug(f"Location: {loc}")
                assert (loc.to_dict() == p)
