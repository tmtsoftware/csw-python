import sys
import os
import json

import structlog
from _pytest import pathlib

from csw.Parameter import Parameter
from csw.CurrentState import CurrentState
from csw.UTCTime import UTCTime
from csw.Units import Units
from csw.Subsystem import Subsystems
from csw.Prefix import Prefix
from csw.LocationService import ComponentType, ConnectionInfo, HttpRegistration, TcpRegistration, \
    AkkaRegistration, ComponentId, ConnectionType, AkkaLocation, HttpLocation, TcpLocation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCswContract:
    log = structlog.get_logger()

    # Validate against Location Service model contract file produced by csw
    def test_location_service_models(self):
        testDir = pathlib.Path(__file__).parent.absolute()
        with open(f"{testDir}/location-models.json") as json_file:
            data = json.load(json_file)
            for p in data['ComponentType']:
                assert (ComponentType[p].name == p)
            for p in data['Connection']:
                connectionInfo = ConnectionInfo.from_dict(p)
                self.log.debug(f"Connection: {connectionInfo}")
                assert (connectionInfo.to_dict() == p)
            for p in data['Registration']:
                regType = p['_type']
                if regType == "HttpRegistration":
                    registration = HttpRegistration.from_dict(p)
                elif regType == "TcpRegistration":
                    registration = TcpRegistration.from_dict(p)
                elif regType == "AkkaRegistration":
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
                if locType == "AkkaLocation":
                    loc = AkkaLocation.from_dict(p)
                elif locType == "HttpLocation":
                    loc = HttpLocation.from_dict(p)
                elif locType == "TcpLocation":
                    loc = TcpLocation.from_dict(p)
                self.log.debug(f"Location: {loc}")
                assert (loc.to_dict() == p)

    # Validate against Command Service model contract file produced by csw
    def test_command_service_models(self):
        testDir = pathlib.Path(__file__).parent.absolute()
        with open(f"{testDir}/command-models.json") as json_file:
            data = json.load(json_file)
            for p in data['Units']:
                assert (Units[p].name == p)
            for p in data['UTCTime']:
                t1 = UTCTime.from_str(p)
                t2 = UTCTime.from_str(str(t1))
                assert (t1 == t2)
            for p in data['CurrentState']:
                cs = CurrentState._fromDict(p)
                assert (str(cs.prefix) == "CSW.ncc.trombone")
                assert (str(cs.stateName) == "idle")
                assert (len(cs.paramSet) == 25)
                for entry in p['paramSet']:
                    for key in entry:
                        # Round-trip test
                        # (ignore time values since resolution of fractional seconds is different in Typescript!)
                        if key not in ['UTCTimeKey', 'TAITimeKey']:
                            assert (entry == Parameter._fromDict(entry)._asDict())
