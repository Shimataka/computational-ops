from computational_ops.core.instruction import Instruction
from computational_ops.core.result import Ok, Result
from computational_ops.core.task import Task, TaskOutput


class TaskB(Task):
    def __init__(self) -> None:
        super().__init__(name="TaskB")

    async def run(
        self,
        from_yaml: Instruction,
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        print("TaskB is running")
        return Ok(TaskOutput(data={"task_b": "TaskB is running"}))
