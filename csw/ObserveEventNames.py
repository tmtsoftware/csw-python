from typing import Self

from csw.EventName import EventName


class ObserveEventNames:

    @staticmethod
    def _eventName(name: str) -> EventName:
        return EventName(f"ObserveEvent.{name}")

    # common
    ObserveStart: EventName = _eventName("ObserveStart")
    ObserveEnd: EventName = _eventName("ObserveEnd")
    ExposureStart: EventName = _eventName("ExposureStart")
    ExposureEnd: EventName = _eventName("ExposureEnd")
    ReadoutEnd: EventName = _eventName("ReadoutEnd")
    ReadoutFailed: EventName = _eventName("ReadoutFailed")
    DataWriteStart: EventName = _eventName("DataWriteStart")
    DataWriteEnd: EventName = _eventName("DataWriteEnd")
    ExposureAborted: EventName = _eventName("ExposureAborted")
    PrepareStart: EventName = _eventName("PrepareStart")

    # IRDetector specific
    IRDetectorExposureData: EventName = _eventName("IRDetectorExposureData")
    IRDetectorExposureState: EventName = _eventName("IRDetectorExposureState")

    # OpticalDetector specific
    OpticalDetectorExposureData: EventName = _eventName("OpticalDetectorExposureData")
    OpticalDetectorExposureState: EventName = _eventName("OpticalDetectorExposureState")

    # WFSDetector specific
    WfsDetectorExposureState: EventName = _eventName("WfsDetectorExposureState")
    PublishSuccess: EventName = _eventName("PublishSuccess")
    PublishFail: EventName = _eventName("PublishFail")

    # Sequencer specific
    PresetStart: EventName = _eventName("PresetStart")
    PresetEnd: EventName = _eventName("PresetEnd")
    GuidestarAcqStart: EventName = _eventName("GuidestarAcqStart")
    GuidestarAcqEnd: EventName = _eventName("GuidestarAcqEnd")
    ScitargetAcqStart: EventName = _eventName("ScitargetAcqStart")
    ScitargetAcqEnd: EventName = _eventName("ScitargetAcqEnd")
    ObservationStart: EventName = _eventName("ObservationStart")
    ObservationEnd: EventName = _eventName("ObservationEnd")
    ObservePaused: EventName = _eventName("ObservePaused")
    ObserveResumed: EventName = _eventName("ObserveResumed")
    DowntimeStart: EventName = _eventName("DowntimeStart")
    OffsetStart: EventName = _eventName("OffsetStart")
    OffsetEnd: EventName = _eventName("OffsetEnd")
    InputRequestStart: EventName = _eventName("InputRequestStart")
    InputRequestEnd: EventName = _eventName("InputRequestEnd")

    # DMS specific
    MetadataAvailable: EventName = _eventName("MetadataAvailable")
    ExposureAvailable: EventName = _eventName("ExposureAvailable")
