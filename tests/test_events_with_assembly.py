import filecmp
import sys
import os
import time

import structlog
from _pytest import pathlib

from csw.KeyType import KeyType
from csw.Units import Units
from csw.EventSubscriber import EventSubscriber
from csw.EventTime import EventTime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
from csw.Parameter import Parameter
from csw.Event import SystemEvent, EventName
from csw.EventPublisher import EventPublisher
from csw.Prefix import Prefix
from csw.Subsystem import Subsystems
from csw.EventKey import EventKey


# Test that publishes events for an assembly running in the background (see ./testSupport).
# Note: Requires that CSW event service is running (csw-services start) and the test assembly
# has been compiled and started. See README.md.
# The assembly writes the received events as JSON to "/tmp/PyTestAssemblyEventHandlers.out" and we compare with
# a known, valid copy. To test the subscriber API, another file "/tmp/PyTestAssemblyEventHandlers.in" is
# generated from the received events here.
class TestEventsWithAssembly:
    log = structlog.get_logger()
    dir = pathlib.Path(__file__).parent.absolute()
    inFileName = "PyTestAssemblyEventHandlers.in"
    outFileName = "PyTestAssemblyEventHandlers.out"
    tmpInFile = f"/tmp/{inFileName}"
    tmpOutFile = f"/tmp/{outFileName}"
    inFile = f"{dir}/{inFileName}"
    outFile = f"{dir}/{outFileName}"
    pub = EventPublisher()
    sub = EventSubscriber()
    prefix = Prefix(Subsystems.CSW, "TestPublisher")

    # def setup_method(self):
    #     self.cleanup()

    def teardown_method(self):
        # pass
        self.cleanup()

    def cleanup(self):
        if os.path.exists(self.tmpInFile):
            os.remove(self.tmpInFile)
        if os.path.exists(self.tmpOutFile):
            os.remove(self.tmpOutFile)

    def test_pub_sub(self):
        time.sleep(1.0)
        self.log.debug("Starting test...")
        thread = self.sub.subscribe(
            [EventKey(self.prefix, EventName("testEvent1")),
             EventKey(self.prefix, EventName("testEvent2")),
             EventKey(self.prefix, EventName("testEvent3"))],
            self.callback)
        try:
            self.publishEvent1()
            self.publishEvent2()
            self.publishEvent3()
            self.log.debug("Published three events...")
            # make sure assembly has time to write the file
            time.sleep(3)
            # compare file created from received events below with known good version
            assert filecmp.cmp(self.inFile, self.tmpInFile, False)
            # compare file created by assembly with known good version
            assert filecmp.cmp(self.outFile, self.tmpOutFile, False)
            self.log.info("Event pub/sub tests passed")
        finally:
            self.log.debug("Stopping subscriber...")
            thread.stop()

    def publishEvent1(self):
        keyName = "assemblyEventValue"
        keyType = KeyType.DoubleKey
        values = [42.0]
        param = Parameter(keyName, keyType, values)
        paramSet = [param]
        event = SystemEvent(self.prefix, EventName("testEvent1"), paramSet)
        self.log.debug(f"Publishing event {event}")
        self.pub.publish(event)

    def publishEvent2(self):
        intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
        intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                                    Units.marcsec)
        intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        event = SystemEvent(self.prefix, EventName("testEvent2"), paramSet)
        self.pub.publish(event)

    def publishEvent3(self):
        intParam = Parameter("IntValue", KeyType.IntKey, [42], Units.arcsec)
        floatParam = Parameter("floatValue", KeyType.FloatKey, [float(42.1)], Units.arcsec)
        longParam = Parameter("longValue", KeyType.LongKey, [42], Units.arcsec)
        shortParam = Parameter("shortValue", KeyType.ShortKey, [42], Units.arcsec)
        byteParam = Parameter("byteValue", KeyType.ByteKey, b'\xDE\xAD\xBE\xEF')
        booleanParam = Parameter("booleanValue", KeyType.BooleanKey, [True, False], Units.arcsec)

        intArrayParam = Parameter("IntArrayValue", KeyType.IntArrayKey, [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", KeyType.FloatArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                                    Units.arcsec)
        doubleArrayParam = Parameter("DoubleArrayValue", KeyType.DoubleArrayKey, [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]],
                                     Units.arcsec)

        byteArrayParam = Parameter("ByteArrayValue", KeyType.ByteArrayKey, [b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4])])

        intMatrixParam = Parameter("IntMatrixValue", KeyType.IntMatrixKey,
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], Units.meter)

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234,
                                                 "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = Parameter("CoordParam", KeyType.CoordKey,
                                [eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord, altAzCoord])

        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam]
        event = SystemEvent(self.prefix, EventName("testEvent3"), paramSet)
        self.pub.publish(event)

    # Event subscriber callback
    def callback(self, systemEvent):
        self.log.debug(f"Received system event '{systemEvent}'")
        # Save event to file as JSON like dict (Not JSON, since byte arrays are not serializable in python),
        # but change the date and id for comparison
        systemEvent.eventId = "test"
        systemEvent.eventTime = EventTime(0, 0)
        mode = "w" if (systemEvent.eventName.name == "testEvent1") else "a"
        f = open(self.tmpInFile, mode)
        jsonStr = str(systemEvent._asDict())
        f.write(f"{jsonStr}\n")
        f.close()
