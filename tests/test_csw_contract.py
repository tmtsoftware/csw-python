import sys
import os
import time
import json

import structlog

from csw.LocationService import ComponentType, ConnectionInfo, HttpRegistration, TcpRegistration, \
    AkkaRegistration

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCswContract:
    log = structlog.get_logger()

    # Validate against contract file produced by csw
    def test_location_service_models(self):
        with open('location_models.json') as json_file:
            data = json.load(json_file)
            for p in data['ComponentType']:
                assert (ComponentType[p].value == p)
            for p in data['Connection']:
                connectionInfo = ConnectionInfo.from_dict(p)
                self.log.debug(f"Connection: {connectionInfo}")
                assert (connectionInfo.to_dict() == p)
            for p in data['Registration']:
                regType = p['_type']
                self.log.debug(f"XXX regType = {regType} ({regType.__class__})")
                # TODO: for Python-3.10.x
                # match regType:
                #     case "HttpRegistration":
                #         registration = HttpRegistration.from_dict(p)
                #     case "TcpRegistration":
                #         registration = TcpRegistration.from_dict(p)
                #     case "AkkaRegistration":
                #         registration = AkkaRegistration.from_dict(p)
                if (regType == "HttpRegistration"):
                        registration = HttpRegistration.from_dict(p)
                elif (regType == "TcpRegistration"):
                        registration = TcpRegistration.from_dict(p)
                elif (regType == "AkkaRegistration"):
                        registration = AkkaRegistration.from_dict(p)
                self.log.debug(f"XXX registration = {registration} ({registration.__class__})")
                assert (registration.to_dict() == p)
