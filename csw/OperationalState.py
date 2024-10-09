from csw.EnumUtil import UpperCaseEnum


class OperationalState(UpperCaseEnum):
    """
    Enumeration indicating if the detector system is available and operational.
     READY, BUSY, ERROR.
     READY indicates system can execute exposures.
     BUSY indicates system is BUSY most likely acquiring data.
     ERROR indicates the detector system is in an error state.
     This could  happen as a result of a command or a spontaneous failure.
     Corrective  action is required.
    """

    READY = 1
    NOT_READY = 2
    ERROR = 3
    BUSY = 4
