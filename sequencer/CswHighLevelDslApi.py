from dataclasses import dataclass
from typing import Callable

from csw.CoordinateSystem import CoordinateSystem
from csw.Event import ObserveEvent
from csw.ExposureId import ExposureId
from csw.ObsId import ObsId
from csw.Prefix import Prefix
from csw.SequencerObserveEvent import SequencerObserveEvent
from csw.Subsystem import Subsystem
from esw.ObsMode import ObsMode
from esw.Variation import Variation
from sequencer.ConfigServiceDsl import ConfigServiceDsl
from sequencer.CswServices import CswServices
from sequencer.EventServiceDsl import EventServiceDsl
from sequencer.LocationServiceDsl import LocationServiceDsl
from sequencer.ScriptContext import ScriptContext


class CswHighLevelDsl(LocationServiceDsl,
                      ConfigServiceDsl,
                      EventServiceDsl,
                      # LoggingDsl,
                      # CommandServiceDsl,
                      # AlarmServiceDsl,
                      # TimeServiceDsl,
                      # DatabaseServiceDsl,
                      # LoopDsl
                      ):
    """
    Interface which contains methods to create different observe events by delegating to DSL of creating observe events
    and has abstract methods to create FSM, CommandFlag, command service for Sequencer, Assembly and Hcd
    """

    def __init__(self, cswServices: CswServices, scriptContext: ScriptContext):
        super().__init__()

    def presetStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of the preset phase of acquisition

        Args:
            obsId (ObsId) Represents a unique observation id
        """
        return self.sequencerObserveEvent.presetStart(obsId)

    def presetEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of the preset phase of  acquisition

        Args:
            obsId (ObsId): Represents a unique observation id
        """
        return self.sequencerObserveEvent.presetEnd(obsId)

    def guidestarAcqStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of locking the telescope to the  sky with guide and WFS targets

        Args:
            obsId: Represents a unique observation id
        """
        return self.sequencerObserveEvent.guidestarAcqStart(obsId)

    def guidestarAcqEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of locking the telescope to the sky with guide and WFS targets
        """
        return self.sequencerObserveEvent.guidestarAcqEnd(obsId)

    def scitargetAcqStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of acquisition phase where  science target is peaked up as needed after  guidestar locking
        """
        return self.sequencerObserveEvent.scitargetAcqStart(obsId)

    def scitargetAcqEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of acquisition phase where  science target is centered as needed after  guidestar locking
        """
        return self.sequencerObserveEvent.scitargetAcqEnd(obsId)

    def observationStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of execution of actions related  to an observation including acquisition and  science data acquisition.
        """
        return self.sequencerObserveEvent.observationStart(obsId)

    def observationEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of execution of actions related  to an observation including acquisition and  science data acquisition.
        """
        return self.sequencerObserveEvent.observationEnd(obsId)

    def observeStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of execution of actions related  to an Observe command
        """
        return self.sequencerObserveEvent.observeStart(obsId)

    def observeEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of execution of actions related  to an Observe command
        """
        return self.sequencerObserveEvent.observeEnd(obsId)

    def exposureStart(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates the start of data acquisition that  results in a file produced for DMS. This is a potential metadata event for DMS.
        """
        return self.sequencerObserveEvent.exposureStart(exposureId)

    def exposureEnd(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates the end of data acquisition that results  in a file produced for DMS. This is a potential metadata event for DMS.
        """
        return self.sequencerObserveEvent.exposureEnd(exposureId)

    def readoutEnd(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a readout that is part of a ramp  has completed.
        """
        return self.sequencerObserveEvent.readoutEnd(exposureId)

    def readoutFailed(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a readout that is part of a ramp has failed indicating transfer failure or some  other issue.
        """
        return self.sequencerObserveEvent.readoutFailed(exposureId)

    def dataWriteStart(self, exposureId: ExposureId, filename: str) -> ObserveEvent:
        """
        This event indicates that the instrument has started writing the exposure data file or transfer of exposure  data to DMS.
        """
        return self.sequencerObserveEvent.dataWriteStart(exposureId, filename)

    def dataWriteEnd(self, exposureId: ExposureId, filename: str) -> ObserveEvent:
        """
        This event indicates that the instrument has finished  writing the exposure data file or transfer of  exposure data to DMS.
        """
        return self.sequencerObserveEvent.dataWriteEnd(exposureId, filename)

    def prepareStart(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates the start of data acquisition that  results in a file produced for DMS. This is a potential metadata event for DMS.
        """
        return self.sequencerObserveEvent.prepareStart(exposureId)

    def exposureAborted(self, exposureId: ExposureId) -> ObserveEvent:
        """
        This event indicates that a request was made to abort the  exposure and it has completed. Normal data events should occur if data is  recoverable.
        """
        return self.sequencerObserveEvent.observePaused()

    def observePaused(self) -> ObserveEvent:
        """
        This event indicates that a user has paused the current  observation Sequence which will happen after  the current step concludes
        """
        return self.sequencerObserveEvent.observePaused()

    def observeResumed(self) -> ObserveEvent:
        """
        This event indicates that a user has resumed a paused  observation Sequence.
        """
        return self.sequencerObserveEvent.observeResumed()

    def downtimeStart(self, obsId: ObsId, reasonForDowntime: str) -> ObserveEvent:
        """
        This event indicates that something has occurred that  interrupts the normal observing workflow and  time accounting.
        This event will have a hint (TBD) that indicates  the cause of the downtime for statistics.
        Examples are: weather, equipment or other  technical failure, etc.
        Downtime is ended by the start of an observation  or exposure.

        Args:
            obsId: Represents a unique observation id
            reasonForDowntime: a hint that indicates the cause of the downtime for statistics
        """
        return self.sequencerObserveEvent.downtimeStart(obsId, reasonForDowntime)

    def offsetStart(self, obsId: ObsId, coordinateSystem: CoordinateSystem, p: float, q: float) -> ObserveEvent:
        """
        This event indicates the start of a telescope offset or dither

        Args:
            obsId: representing a unique observation id
            coordinateSystem: type of (p, q) coords
            p: Represents telescope's xCoordinate offset
            q: Represents telescope's yCoordinate offset
        """
        return self.sequencerObserveEvent.offsetStart(obsId, coordinateSystem, p, q)

    def offsetEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of a telescope offset or dither
        """
        return self.sequencerObserveEvent.offsetEnd(obsId)

    def inputRequestStart(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the start of a request to the user for input
        """
        return self.sequencerObserveEvent.inputRequestStart(obsId)

    def inputRequestEnd(self, obsId: ObsId) -> ObserveEvent:
        """
        This event indicates the end of a request to the user for input
        """
        return self.sequencerObserveEvent.inputRequestEnd(obsId)

    def Assembly(self, prefix: Prefix, defaultTimeoutSecs: int = 10) -> RichComponent:
        """
        Creates an instance of RichComponent for Assembly of given prefix

        Args:
            prefix: prefix of Assembly
            defaultTimeoutSecs: default timeout for the response of the RichComponent's API in secs

        Returns:
            a RichComponent instance
        """
        pass

    def Assembly2(self, subsystem: Subsystem, compName: str, defaultTimeoutSecs: int = 10) -> RichComponent:
        return self.Assembly(Prefix(subsystem, compName), defaultTimeoutSecs)

    def Hcd(prefix: Prefix, defaultTimeoutSecs: int = 10) -> RichComponent:
        """
        Creates an instance of RichComponent for HCD of given prefix
        """
        pass

    def Hcd2(self, subsystem: Subsystem, compName: str, defaultTimeoutSecs: int = 10) -> RichComponent:
        return self.Hcd(Prefix(subsystem, compName), defaultTimeoutSecs)

    def Sequencer(subsystem: Subsystem, obsMode: ObsMode) -> RichSequencer:
        """
        Creates an instance of RichSequencer for Sequencer of given subsystem and obsMode
        """
        pass

    def Sequencer2(subsystem: Subsystem, obsMode: ObsMode, defaultTimeoutSecs: int) -> RichSequencer:
        """
        Creates an instance of RichSequencer for Sequencer of given subsystem and obsMode
        """
        pass

    def Sequencer3(subsystem: Subsystem, obsMode: ObsMode, variation: Variation) -> RichSequencer:
        """
        Creates an instance of RichSequencer for Sequencer of given subsystem and obsMode
        """
        pass

    def Sequencer4(subsystem: Subsystem, obsMode: ObsMode, variation: Variation,
                   defaultTimeoutSecs: int) -> RichSequencer:
        """
        Creates an instance of RichSequencer for Sequencer of given subsystem and obsMode
        """

    def Fsm(name: str, initState: str, func: Callable[[FsmScope], None]) -> Fsm:
        pass

    def commandFlag() -> CommandFlag:
        pass

    # /**
    #  * Method to create an instance of [[esw.ocs.dsl.epics.ParamVariable]] tied to the particular param `key` of an [[csw.params.events.Event]]
    #  * being published on specific `event key`.
    #  *
    #  * [[esw.ocs.dsl.epics.ParamVariable]] is [[esw.ocs.dsl.epics.EventVariable]] with methods to get and set a specific parameter in the [[csw.params.events.Event]]
    #  *
    #  * It behaves differently depending on the presence of `duration` parameter while creating its instance.
    #  * - When provided with `duration`, it will **poll** at an interval of given `duration` to refresh its own value
    #  * - Otherwise it will **subscribe** to the given event key and will refresh its own value whenever events are published
    #  *
    #  * @param initial value to set to the parameter key of the event
    #  * @param eventKeyStr string representation of event key
    #  * @param key represents parameter key of the event to tie [[esw.ocs.dsl.epics.ParamVariable]] to
    #  * @param duration represents the interval of polling.
    #  * @return instance of [[esw.ocs.dsl.epics.ParamVariable]]
    #  */
    # def <T> ParamVariable(initial: T, eventKeyStr: str, key: Key<T>, duration: Duration? = null): ParamVariable<T> =
    #         ParamVariable.make(initial, key, EventKey.apply(eventKeyStr), this, duration)

    # /**
    #  * Method to create an instance of [[esw.ocs.dsl.epics.EventVariable]] tied to an [[csw.params.events.Event]] being published on specified `event key`.
    #  *
    #  * [[esw.ocs.dsl.epics.EventVariable]] behaves differently depending on the presence of `duration` parameter while creating its instance.
    #  * - When provided with `duration`, it will **poll** at an interval of given `duration` to refresh its own value
    #  * - Otherwise it will **subscribe** to the given event key and will refresh its own value whenever events are published
    #  *
    #  * @param eventKeyStr string representation of event key
    #  * @param duration represents the interval of polling.
    #  * @ return instance of [[esw.ocs.dsl.epics.EventVariable]]
    #  */
    # suspend def EventVariable(eventKeyStr: str, duration: Duration? = null): EventVariable =
    #         EventVariable.make(EventKey.apply(eventKeyStr), this, duration)

    def finishWithError(message: str = ""):
        raise RuntimeError(message)
