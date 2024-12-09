import asyncio
from asyncio import Task

from csw.CommandResponse import CommandResponse, Error


class CommandResponseManager:
    """
    Keeps track of command responses for long running commands by maintaining a
    map from runId to CommandResponse.
    """
    tasks = {}

    def addTask(self, runId: str, task: Task):
        self.tasks[runId] = task

    async def waitForTask(self, runId: str, timeoutInSeconds: int) -> CommandResponse:
        if runId in self.tasks:
            task: Task = self.tasks[runId]
            return await asyncio.wait_for(task, timeout=timeoutInSeconds*1.0)
        else:
            return Error(runId, "No task was found for runId " + runId)
