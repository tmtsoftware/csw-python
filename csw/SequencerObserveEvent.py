from dataclasses import dataclass

from csw.CoordinateSystem import CoordinateSystem
from csw.Event import ObserveEvent
from csw.EventName import EventName
from csw.ExposureId import ExposureId
from csw.ObsId import ObsId
from csw.ObserveEventNames import ObserveEventNames
from csw.ParamFactories import ParamFactories
from csw.Prefix import Prefix


@dataclass
class SequencerObserveEvent:
    """
    The events that indicate activities for each observation and the acquisition process.

    Args:
        prefix: the prefix identifier of the sequencer which is generating this event
    """
    prefix: Prefix

    def presetStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of the preset phase of  acquisition

        Args:
            obsId: Represents a unique observation id
        """
        return self._createObserveEvent(ObserveEventNames.PresetStart, obsId)

    def presetEnd(self, obsId: ObsId) -> ObserveEvent:
        """
          This event indicates the end of the preset phase of  acquisition

        Args:
            obsId: Represents a unique observation id
        """
        return self._createObserveEvent(ObserveEventNames.PresetEnd, obsId)

    def guidestarAcqStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of locking the telescope to the  sky with guide and WFS targets

        Args:
            obsId: Represents a unique observation id
        """
        return self._createObserveEvent(ObserveEventNames.GuidestarAcqStart, obsId)

    def guidestarAcqEnd(self, obsId: ObsId) -> ObserveEvent:
        """
       This event indicates the end of locking the telescope to the sky with guide and WFS targets

        Args:
            obsId: Represents a unique observation id
        """
        return self._createObserveEvent(ObserveEventNames.GuidestarAcqEnd, obsId)

    def scitargetAcqStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of acquisition phase where  science target is peaked up as needed after  guidestar locking

        Args:
            obsId: Represents a unique observation id

        Returns:

        """
        return self._createObserveEvent(ObserveEventNames.ScitargetAcqStart, obsId)

    def scitargetAcqEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of acquisition phase where  science target is centered as needed after  guidestar locking

        Args:
            obsId: Represents a unique observation id

        Returns:

        """
        return self._createObserveEvent(ObserveEventNames.ScitargetAcqEnd, obsId)

    def observationStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of execution of actions related  to an observation including acquisition and  science data acquisition.

        Args:
            obsId: Represents a unique observation id

        Returns:

        """
        return self._createObserveEvent(ObserveEventNames.ObservationStart, obsId)

    def observationEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of execution of actions related  to an observation including acquisition and  science data acquisition.

        Args:
            obsId: Represents a unique observation id

        Returns:

        """
        return self._createObserveEvent(ObserveEventNames.ObservationEnd, obsId)

    def observeStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of execution of actions related  to an Observe command

        Args:
            obsId: Represents a unique observation id

        Returns:

        """
        return self._createObserveEvent(ObserveEventNames.ObserveStart, obsId)

    def observeEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of execution of actions related  to an Observe command

        Args:
            obsId: Represents a unique observation id
        """
        return self._createObserveEvent(ObserveEventNames.ObserveEnd, obsId)

    def exposureStart(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates the start of data acquisition that  results in a file produced for DMS. This is a potential metadata event for DMS.

        Args:
            exposureId:    an identifier in ESW/DMS for a single exposure.
                           The ExposureId follows the structure: 2020A-001-123-WFOS-IMG1-SCI0-0001 with an included ObsId or
                           when no ObsId is present, in the standalone format: 20200706-190204-WFOS-IMG1-SCI0-0001 with a UTC time
                           when the ExposureId is created.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.ExposureStart, exposureId)

    def exposureEnd(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates the end of data acquisition that results  in a file produced for DMS. This is a potential metadata event for DMS.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
                        The ExposureId follows the structure: 2020A-001-123-WFOS-IMG1-SCI0-0001 with an included ObsId or
                        when no ObsId is present, in the standalone format: 20200706-190204-WFOS-IMG1-SCI0-0001 with a UTC time
                        when the ExposureId is created.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.ExposureEnd, exposureId)

    def readoutEnd(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a readout that is part of a ramp  has completed.
        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.ReadoutEnd, exposureId)

    def readoutFailed(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a readout that is part of a ramp  has failed indicating transfer failure or some  other issue.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.ReadoutFailed, exposureId)

    def dataWriteStart(self, exposureId: ExposureId, filename: str) -> ObserveEvent:
        """
        This event indicates that the instrument has started writing  the exposure data file or transfer of exposure  data to DMS.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
            filename: the path of the file

        Returns:

        """
        return self._createObserveEventWithExposureId(ObserveEventNames.DataWriteStart, exposureId, filename)

    def dataWriteEnd(self, exposureId: ExposureId, filename: str) -> ObserveEvent:
        """
        This event indicates that the instrument has finished  writing the exposure data file or transfer of  exposure data to DMS.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
            filename: the path of the file
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.DataWriteEnd, exposureId, filename)

    def prepareStart(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that the detector system is preparing to start an exposure.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.PrepareStart, exposureId)

    def exposureAborted(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a request was made to abort the  exposure and it has completed. Normal data events should occur if data is  recoverable.

        Args:
            exposureId: an identifier in ESW/DMS for a single exposure.
        """
        return self._createObserveEventWithExposureId(ObserveEventNames.ExposureAborted, exposureId)

    def observePaused(self) -> ObserveEvent:
        """
        This event indicates that a user has paused the current  observation Sequence which will happen after  the current step concludes
        """
        return ObserveEvent(self.prefix, ObserveEventNames.ObservePaused, [])

    def observeResumed(self) -> ObserveEvent:
        """
        This event indicates that a user has resumed a paused  observation Sequence.
        """
        return ObserveEvent(self.prefix, ObserveEventNames.ObserveResumed, [])

    def downtimeStart(self, obsId: ObsId, reasonForDowntime: str) -> ObserveEvent:
        """
        This event indicates that something has occurred that  interrupts the normal observing workflow and  time accounting.
        This event will have a hint (TBD) that indicates  the cause of the downtime for statistics.
        Examples are: weather, equipment or other  technical failure, etc.
        Downtime is ended by the start of an observation  or exposure.

        Args:
            obsId: Represents a unique observation id
            reasonForDowntime:  a hint that indicates the cause of the downtime for statistics.

        Returns:

        """
        obsIdParam = ParamFactories.obsIdParam(obsId)
        downtimeReasonParam = ParamFactories.downTimeReasonParam(reasonForDowntime)
        return ObserveEvent(self.prefix, ObserveEventNames.DowntimeStart, [obsIdParam, downtimeReasonParam])

    def offsetStart(self, obsId: ObsId, coordinateSystem: CoordinateSystem, p: float, q: float) -> ObserveEvent:
        """
        This event indicates the start of a telescope offset or dither

        Args:
            obsId: representing a unique observation id
            coordinateSystem: Represents coordinate system
            p: Represents telescope's xCoordinate offset
            q: Represents telescope's yCoordinate offset
        """
        return ObserveEvent(
            self.prefix,
            ObserveEventNames.OffsetStart,
            [
                ParamFactories.obsIdParam(obsId),
                ParamFactories.coordinateSystemParam(coordinateSystem),
                ParamFactories.pOffsetParam(p),
                ParamFactories.qOffsetParam(q)
            ]
        )

    def offsetEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of a telescope offset or dither

        Args:
            obsId: representing a unique observation id
        """
        return ObserveEvent(self.prefix, ObserveEventNames.OffsetEnd, [ParamFactories.obsIdParam(obsId)])

    def inputRequestStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of a request to the user for input

        Args:
            obsId: Representing a unique observation id
        """
        return ObserveEvent(self.prefix, ObserveEventNames.InputRequestStart, [ParamFactories.obsIdParam(obsId)])

    def inputRequestEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of a request to the user for input

        Args:
            obsId: Representing a unique observation id
        """
        return ObserveEvent(self.prefix, ObserveEventNames.InputRequestEnd, [ParamFactories.obsIdParam(obsId)])

    def _createObserveEvent(self, eventName: EventName, obsId: ObsId) -> ObserveEvent:
        params = [ParamFactories.obsIdParam(obsId)]
        return ObserveEvent(self.prefix, eventName, params)

    def _createObserveEventWithExposureId(self, eventName: EventName, exposureId: ExposureId,
                                          filename: str = None) -> ObserveEvent:
        params = [ParamFactories.exposureIdParam(exposureId)]
        if not filename is None:
            params.append(ParamFactories.filenameParam(filename))
        return ObserveEvent(self.prefix, eventName, params)
