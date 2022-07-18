import filecmp
import os
import time

import structlog
from _pytest import pathlib

from csw.EventSubscriber import EventSubscriber
from csw.EventTime import EventTime
from csw.Parameter import *

from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
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
            self.publishEvent4()
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
        param = DoubleKey.make("assemblyEventValue").set(42.0)
        paramSet = [param]
        event = SystemEvent(self.prefix, EventName("testEvent1"), paramSet)
        self.log.debug(f"Publishing event {event}")
        self.pub.publish(event)

    def publishEvent2(self):
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue", Units.mas).set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])
        paramSet = [intParam, intArrayParam, floatArrayParam, intMatrixParam]
        event = SystemEvent(self.prefix, EventName("testEvent2"), paramSet)
        self.pub.publish(event)

    def publishEvent3(self):
        intParam = IntKey.make("IntValue", Units.arcsec).set(42)
        floatParam = FloatKey.make("floatValue", Units.arcsec).set(42.1)
        longParam = LongKey.make("longValue", Units.arcsec).set(42)
        shortParam = ShortKey.make("shortValue", Units.arcsec).set(42)
        byteParam = ByteKey.make("byteValue").set(0xDE, 0xAD, 0xBE, 0xEF)
        booleanParam = BooleanKey.make("booleanValue").set(True, False)

        intArrayParam = IntArrayKey.make("IntArrayValue").set([1, 2, 3, 4], [5, 6, 7, 8])
        floatArrayParam = FloatArrayKey.make("FloatArrayValue", Units.arcsec).set([1.2, 2.3, 3.4], [5.6, 7.8, 9.1])
        doubleArrayParam = DoubleArrayKey.make("DoubleArrayValue", Units.arcsec).setAll(
            [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]])
        byteArrayParam = ByteArrayKey.make("ByteArrayValue").set(b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4]))
        intMatrixParam = IntMatrixKey.make("IntMatrixValue", Units.meter).set([[1, 2, 3, 4], [5, 6, 7, 8]],
                                                                              [[-1, -2, -3, -4], [-5, -6, -7, -8]])

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234, "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = CoordKey.make("CoordParam").set(eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord,
                                                      altAzCoord)
        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam]
        event = SystemEvent(self.prefix, EventName("testEvent3"), paramSet)
        self.pub.publish(event)

    def publishEvent4(self):
        param = UTCTimeKey.make("assemblyEventValue").set(UTCTime.from_str("2021-09-20T20:43:35.419053077Z"))
        param2 = TAITimeKey.make("assemblyEventValue2").set(TAITime.from_str("2021-09-20T18:44:12.419084072Z"))
        paramSet = [param, param2]
        event = SystemEvent(self.prefix, EventName("testEvent4"), paramSet)
        self.log.debug(f"Publishing event {event}")
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
