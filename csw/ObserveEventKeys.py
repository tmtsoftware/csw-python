from csw.CoordinateSystem import CoordinateSystem
from csw.OperationalState import OperationalState
from csw.Parameter import Key, StringKey, GChoiceKey, ChoiceKey, BooleanKey, LongKey, IntKey, DoubleKey
from csw.Units import Units


class ObserveEventKeys:
    obsId: Key[str] = StringKey.make("obsId")
    exposureId: Key[str] = StringKey.make("exposureId")
    detector: Key[str] = StringKey.make("detector")
    operationalState: GChoiceKey = ChoiceKey.make("operationalState", OperationalState.list())
    errorMessage: Key[str] = StringKey.make("errorMessage")
    exposureInProgress: Key[bool] = BooleanKey.make("exposureInProgress")
    abortInProgress: Key[bool] = BooleanKey.make("abortInProgress")
    isAborted: Key[bool] = BooleanKey.make("isAborted")
    exposureTime: Key[int] = LongKey.make("exposureTime", Units.millisecond)
    remainingExposureTime: Key[int] = LongKey.make("remainingExposureTime", Units.millisecond)
    readsInRamp: Key[int] = IntKey.make("readsInRamp")
    readsComplete: Key[int] = IntKey.make("readsComplete")
    rampsInExposure: Key[int] = IntKey.make("rampsInExposure")
    rampsComplete: Key[int] = IntKey.make("rampsComplete")
    coaddsInExposure: Key[int] = IntKey.make("coaddsInExposure")
    coaddsDone: Key[int] = IntKey.make("coaddsDone")
    downTimeReason: Key[str] = StringKey.make("reason")
    filename: Key[str] = StringKey.make("filename")
    pOffSet: Key[float] = DoubleKey.make("p", Units.arcsec)
    qOffSet: Key[float] = DoubleKey.make("q", Units.arcsec)
    coordinateSystem: GChoiceKey = ChoiceKey.make("coordinateSystem", CoordinateSystem.list())
