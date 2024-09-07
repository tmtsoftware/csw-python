from csw.ParameterSetType import SequenceCommand
from csw.UTCTime import UTCTime


class ScriptApi:
    """
    This is the API for a sequencer script
    """

    def execute(self, command: SequenceCommand):
        """
        Executes the script's handler (handler with the same name as Command) with the command

        Args:
            command (SequenceCommand): A sequence command to be used to call the handler
        """
        pass

    def executeGoOnline(self):
        """
        Executes the script's onGoOnline handler
        """
        pass

    def executeGoOffline(self):
        """
        Executes the script's onGoOffline handler
        """
        pass

    def executeShutdown(self):
        """
        Executes the script's onShutdown handler
        """
        pass

    def executeAbort(self):
        """
        Executes the script's onAbortSequence handler
        """
        pass

    def executeNewSequenceHandler(self):
        """
        Executes the script's onNewSequence handler
        """
        pass

    def executeStop(self):
        """
        Executes the script's onStop handler
        """
        pass

    def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Executes the script's onDiagnosticMode handler
        """
        pass

    def executeOperationsMode(self):
        """
        Executes the script's onOperationsMode handler
        """
        pass

    def executeExceptionHandlers(self):
        """
        Executes the script's onException handler
        """
        pass

    def shutdownScript(self):
        """
        Runs the shutdown runnable(some extra tasks while unloading the script)
        """
        pass
