
# XXX TODO FIXME
class AlarmService:
    """
    An AlarmService interface to set severity of alarms
    """

    # def setSeverity(key: AlarmKey, severity: AlarmSeverity):
    #     """
    #     Sets the severity of an alarm. It also internally updates the latch severity and acknowledgement status. The
    #     severity is set in alarm store with a specific TTL (time to live). After the time passes for TTL, the severity
    #     will be automatically inferred as `Disconnected`.
    #
    #     Note: By default all alarms are loaded in alarm store as `Disconnected`. Once the component is up and working,
    #           it will be it's responsibility to update all it's alarms with appropriate severity and keep refreshing it.
    #
    #     Args:
    #         key: represents a unique alarm in alarm store e.g nfiraos.trombone.tromboneaxislowlimitalarm
    #         severity: represents the severity to be set for the alarm e.g. Okay, Warning, Major, Critical, etc
    #
    #     Returns:
    #         a task which completes when the severity is successfully set in alarm store or fails with
    #         InvalidSeverityException or KeyNotFoundException
    #     """
    #     pass
    #
