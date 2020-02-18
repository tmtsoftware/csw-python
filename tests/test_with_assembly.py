import filecmp
import json
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
# Requires that CSW services and the test assembly are running.
# The assembly writes the received events as JSON to "/tmp/PyTestAssemblyHandlers.out" and we compare with
# a known, valid copy. To test the subscriber API, another file "/tmp/PyTestAssemblyHandlers.in" is
# generated from the received events here.
def test_pub_sub():
    pub = EventPublisher()
    sub = EventSubscriber()
    prefix = "CSW.TestPublisher"
    thread = sub.subscribe([prefix + "." + "testEvent1", prefix + "." + "testEvent2", prefix + "." + "testEvent3"], callback)
    publishEvent1(prefix, pub)
    publishEvent2(prefix, pub)
    publishEvent3(prefix, pub)
    # make sure assembly has time to write the file
    time.sleep(0.5)
    dir = pathlib.Path(__file__).parent.absolute()
    # compare file created by assembly with known good version
    assert filecmp.cmp(f"{dir}/PyTestAssemblyHandlers.out", "/tmp/PyTestAssemblyHandlers.out")
    # compare file created from received events below with known good version
    assert filecmp.cmp(f"{dir}/PyTestAssemblyHandlers.in", "/tmp/PyTestAssemblyHandlers.in")
    thread.stop()

def publishEvent1(prefix: str, pub: EventPublisher):
    keyName = "assemblyEventValue"
    keyType = 'DoubleKey'
    values = [42.0]
    param = Parameter(keyName, keyType, values)
    paramSet = [param]
    event = SystemEvent(prefix, "testEvent1", paramSet)
    pub.publish(event)

def publishEvent2(prefix: str, pub: EventPublisher):
    intParam = Parameter("IntValue", "IntKey", [42], "arcsec")
    intArrayParam = Parameter("IntArrayValue", "IntArrayKey", [[1,2,3,4], [5,6,7,8]])
    floatArrayParam = Parameter("FloatArrayValue", "FloatArrayKey", [[1.2, 2.3, 3.4], [5.6, 7.8, 9.1]], "marcsec")
    intMatrixParam = Parameter("IntMatrixValue", "IntMatrixKey", [[[1,2,3,4], [5,6,7,8]],[[-1,-2,-3,-4], [-5,-6,-7,-8]]], "meter")
    event = SystemEvent(prefix, "testEvent2", [intParam, intArrayParam, floatArrayParam, intMatrixParam])
    pub.publish(event)

def publishEvent3(prefix: str, pub: EventPublisher):
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
def callback(systemEvent):
    print(f"Received system event '{systemEvent.eventName}'")
    # Save event to file as JSON like dict (Not JSON, since byte arrays are not serializable in python),
    # but change the date and id for comparison
    systemEvent.eventId = "test"
    systemEvent.eventTime = EventTime(0, 0)
    mode = "w" if (systemEvent.eventName == "testEvent1") else "a"
    f = open("/tmp/PyTestAssemblyHandlers.in", mode)
    jsonStr = str(systemEvent.asDict())
    f.write(f"{jsonStr}\n")
    f.close()

