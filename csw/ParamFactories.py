from csw.CoordinateSystem import CoordinateSystem
from csw.ExposureId import ExposureId
from csw.ObsId import ObsId
from csw.ObserveEventKeys import ObserveEventKeys
from csw.OperationalState import OperationalState
from csw.Parameter import Parameter


class ParamFactories:
    """
    commonly used params factories
    """

    @staticmethod
    def obsIdParam(obsId: ObsId) -> Parameter[str]:
        return ObserveEventKeys.obsId.set(str(obsId))

    @staticmethod
    def exposureIdParam(exposureId: ExposureId) -> Parameter[str]:
        return ObserveEventKeys.exposureId.set(str(exposureId))

    @staticmethod
    def operationalStateParam(operationalState: OperationalState) -> Parameter[str]:
        return ObserveEventKeys.operationalState.set(operationalState.name)

    @staticmethod
    def errorMessageParam(errorMessage: str) -> Parameter[str]:
        return ObserveEventKeys.errorMessage.set(errorMessage)

    @staticmethod
    def exposureInProgressParam(exposureInProgress: bool) -> Parameter[bool]:
        return ObserveEventKeys.exposureInProgress.set(exposureInProgress)

    @staticmethod
    def abortInProgressParam(abortInProgress: bool) -> Parameter[bool]:
        return ObserveEventKeys.abortInProgress.set(abortInProgress)

    @staticmethod
    def isAbortedParam(isAborted: bool) -> Parameter[bool]:
        return ObserveEventKeys.isAborted.set(isAborted)

    @staticmethod
    def exposureTimeParam(exposureTime: int) -> Parameter[int]:
        return ObserveEventKeys.exposureTime.set(exposureTime)

    @staticmethod
    def remainingExposureTimeParam(remainingExposureTime: int) -> Parameter[int]:
        return ObserveEventKeys.remainingExposureTime.set(remainingExposureTime)

    @staticmethod
    def readsInRampParam(readsInRamp: int) -> Parameter[int]:
        return ObserveEventKeys.readsInRamp.set(readsInRamp)

    @staticmethod
    def readsCompleteParam(readsComplete: int) -> Parameter[int]:
        return ObserveEventKeys.readsComplete.set(readsComplete)

    @staticmethod
    def rampsInExposureParam(rampsInExposure: int) -> Parameter[int]:
        return ObserveEventKeys.rampsInExposure.set(rampsInExposure)

    @staticmethod
    def rampsCompleteParam(rampsComplete: int) -> Parameter[int]:
        return ObserveEventKeys.rampsComplete.set(rampsComplete)

    @staticmethod
    def coaddsInExposureParam(coaddsInExposure: int) -> Parameter[int]:
        return ObserveEventKeys.coaddsInExposure.set(coaddsInExposure)

    @staticmethod
    def coaddsDoneParam(coaddsDone: int) -> Parameter[int]:
        return ObserveEventKeys.coaddsDone.set(coaddsDone)

    @staticmethod
    def downTimeReasonParam(reasonForDownTime: str) -> Parameter[str]:
        return ObserveEventKeys.downTimeReason.set(reasonForDownTime)

    @staticmethod
    def filenameParam(filename: str) -> Parameter[str]:
        return ObserveEventKeys.filename.set(filename)

    @staticmethod
    def coordinateSystemParam(coordinateSystem: CoordinateSystem) -> Parameter[str]:
        return ObserveEventKeys.coordinateSystem.set(coordinateSystem.name)

    @staticmethod
    def pOffsetParam(pOffset: float) -> Parameter[float]:
        return ObserveEventKeys.pOffSet.set(pOffset)

    @staticmethod
    def qOffsetParam(qOffset: float) -> Parameter[float]:
        return ObserveEventKeys.qOffSet.set(qOffset)
