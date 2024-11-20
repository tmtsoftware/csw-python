from csw.ParameterSetType import SequenceCommand
from csw.UTCTime import UTCTime


class ScriptApi:
    """
    This is the API for a sequencer script
    """

    async def execute(self, command: SequenceCommand):
        """
        Executes the script's handler (handler with the same name as Command) with the command

        Args:
            command (SequenceCommand): A sequence command to be used to call the handler
        """
        pass

    async def executeGoOnline(self):
        """
        Executes the script's onGoOnline handler
        """
        pass

    async def executeGoOffline(self):
        """
        Executes the script's onGoOffline handler
        """
        pass

    async def executeShutdown(self):
        """
        Executes the script's onShutdown handler
        """
        pass

    async def executeAbort(self):
        """
        Executes the script's onAbortSequence handler
        """
        pass

    async def executeNewSequenceHandler(self):
        """
        Executes the script's onNewSequence handler
        """
        pass

    async def executeStop(self):
        """
        Executes the script's onStop handler
        """
        pass

    async def executeDiagnosticMode(self, startTime: UTCTime, hint: str):
        """
        Executes the script's onDiagnosticMode handler
        """
        pass

    async def executeOperationsMode(self):
        """
        Executes the script's onOperationsMode handler
        """
        pass

    async def executeExceptionHandlers(self, ex: Exception):
        """
        Executes the script's onException handler
        """
        pass

    async def shutdownScript(self):
        """
        Runs the shutdown runnable(some extra tasks while unloading the script)
        """
        pass
