from computational_ops.core.result import Err, Ok, Result
from computational_ops.core.task import Task, TaskOutput


class PipelineSequence:
    """PipelineSequence is a class that sequences the tasks.

    Args:
        from_yaml (Instruction): The instruction to run the task.
    """

    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks

    async def run(self, default_output: TaskOutput) -> Result[TaskOutput, str]:
        output = default_output
        for task in self.tasks:
            result = await task.run(from_pedecessor=output)
            if result.is_err():
                return Err(result.unwrap_err())
            output = result.unwrap()
        return Ok(output)
