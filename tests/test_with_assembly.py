import filecmp
import sys
import os
import time

from _pytest import pathlib

from csw.EventSubscriber import EventSubscriber
from csw.EventTime import EventTime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from csw.Coords import EqCoord, EqFrame, SolarSystemCoord, SolarSystemObject, MinorPlanetCoord, \
    CometCoord, AltAzCoord
from csw.Parameter import Parameter, Struct
from csw.Event import SystemEvent
from csw.EventPublisher import EventPublisher


# Test that publishes events for an assembly running in the background (see ./testSupport).
# Note: Requires that CSW event service is running (csw-services.sh start -es 6379) and the test assembly
# has been compiled and started. See README.md.
# The assembly writes the received events as JSON to "/tmp/PyTestAssemblyHandlers.out" and we compare with
# a known, valid copy. To test the subscriber API, another file "/tmp/PyTestAssemblyHandlers.in" is
# generated from the received events here.
class TestWithAssembly:
    dir = pathlib.Path(__file__).parent.absolute()
    inFileName = "PyTestAssemblyHandlers.in"
    outFileName = "PyTestAssemblyHandlers.out"
    tmpInFile = f"/tmp/{inFileName}"
    tmpOutFile = f"/tmp/{outFileName}"
    inFile = f"{dir}/{inFileName}"
    outFile = f"{dir}/{outFileName}"

    def setup_method(self):
        self.cleanup()

    def teardown_method(self):
        self.cleanup()

    def cleanup(self):
        if os.path.exists(self.tmpInFile):
            os.remove(self.tmpInFile)
        if os.path.exists(self.tmpOutFile):
            os.remove(self.tmpOutFile)

    def test_pub_sub(self):

        time.sleep(1.0)
        print("Starting test...")
        pub = EventPublisher()
        sub = EventSubscriber()
        prefix = "CSW.TestPublisher"
        thread = sub.subscribe([prefix + "." + "testEvent1", prefix + "." + "testEvent2", prefix + "." + "testEvent3"],
                               self.callback)
        try:
            self.publishEvent1(prefix, pub)
            self.publishEvent2(prefix, pub)
            self.publishEvent3(prefix, pub)
            print("Published three events...")
            # make sure assembly has time to write the file
            time.sleep(0.5)
            # compare file created by assembly with known good version
            assert filecmp.cmp(self.outFile, self.tmpOutFile, False)
            # compare file created from received events below with known good version
            assert filecmp.cmp(self.inFile, self.tmpInFile, False)
            print("Event pub/sub tests passed")
        finally:
            print("Stopping subscriber...")
            thread.stop()

    def publishEvent1(self, prefix: str, pub: EventPublisher):
        keyName = "assemblyEventValue"
        keyType = 'DoubleKey'
        values = [42.0]
        param = Parameter(keyName, keyType, values)
        paramSet = [param]
        event = SystemEvent(prefix, "testEvent1", paramSet)
        pub.publish(event)

    def publishEvent2(self, prefix: str, pub: EventPublisher):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")
        event = SystemEvent(prefix, "testEvent2", [intParam, intArrayParam, floatArrayParam, intMatrixParam])
        pub.publish(event)

    def publishEvent3(self, prefix: str, pub: EventPublisher):
        intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
        floatParam = Parameter("floatValue", "FloatKey", [float(42.1)], "arcsec")
        longParam = Parameter("longValue", "LongKey", [42], "arcsec")
        shortParam = Parameter("shortValue", "ShortKey", [42], "arcsec")
        byteParam = Parameter("byteValue", "ByteKey", b'\xDE\xAD\xBE\xEF')
        booleanParam = Parameter("booleanValue", "BooleanKey", [True, False], "arcsec")

        intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1, 2, 3, 4], [5, 6, 7, 8]])
        floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")
        doubleArrayParam = Parameter("DoubleArrayValue", "DoubleArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "arcsec")

        byteArrayParam = Parameter("ByteArrayValue", "ByteArrayKey", [b'\xDE\xAD\xBE\xEF', bytes([1, 2, 3, 4])])

        intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey",
                                   [[[1, 2, 3, 4], [5, 6, 7, 8]], [[-1, -2, -3, -4], [-5, -6, -7, -8]]], "meter")

        eqCoord = EqCoord.make(ra="12:13:14.15 hours", dec="-30:31:32.3 deg", frame=EqFrame.FK5, pm=(0.5, 2.33))
        solarSystemCoord = SolarSystemCoord.make("BASE", SolarSystemObject.Venus)
        minorPlanetCoord = MinorPlanetCoord.make("GUIDER1", 2000, "90 deg", "2 deg", "100 deg", 1.4, 0.234,
                                                 "220 deg")
        cometCoord = CometCoord.make("BASE", 2000.0, "90 deg", "2 deg", "100 deg", 1.4, 0.234)
        altAzCoord = AltAzCoord.make("301 deg", "42.5 deg")
        coordsParam = Parameter("CoordParam", "CoordKey",
                                [eqCoord, solarSystemCoord, minorPlanetCoord, cometCoord, altAzCoord])

        structParam = Parameter("MyStruct", "StructKey", [Struct(
            [coordsParam, intParam, floatParam, longParam, shortParam, booleanParam, intArrayParam, floatArrayParam,
             doubleArrayParam, intMatrixParam])])

        paramSet = [coordsParam, byteParam, intParam, floatParam, longParam, shortParam, booleanParam, byteArrayParam,
                    intArrayParam, floatArrayParam, doubleArrayParam, intMatrixParam, structParam]
        event = SystemEvent(prefix, "testEvent3", paramSet)
        pub.publish(event)

    # Event subscriber callback
    def callback(self, systemEvent):
        print(f"Received system event '{systemEvent.eventName}'")
        # Save event to file as JSON like dict (Not JSON, since byte arrays are not serializable in python),
        # but change the date and id for comparison
        systemEvent.eventId = "test"
        systemEvent.eventTime = EventTime(0, 0)
        mode = "w" if (systemEvent.eventName == "testEvent1") else "a"
        f = open(self.tmpInFile, mode)
        jsonStr = str(systemEvent.asDict())
        f.write(f"{jsonStr}\n")
        f.close()
