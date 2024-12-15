from computational_ops.core.instruction import Instruction
from computational_ops.core.result import Err, Ok, Result
from computational_ops.core.task import Task, TaskOutput


class TemplateTask(Task):
    def __init__(self, from_yaml: Instruction) -> None:
        super().__init__(name="TemplateTask", from_yaml=from_yaml)

    def validate_yaml(self, from_yaml: Instruction) -> Result[Instruction, str]:
        result = some_check(from_yaml)
        if result.is_err():
            return Err(result.unwrap_err())
        return Ok(from_yaml)

    async def run(
        self,
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        print("TemplateTask is running")
        result = await some_function(self.from_yaml, from_pedecessor)
        if result.is_err():
            return Err(result.unwrap_err())
        print("TemplateTask is done")
        return Ok(result.unwrap())


def some_check(from_yaml: Instruction) -> Result[Instruction, str]:
    print("some_check is running")
    print(from_yaml)
    return Ok(from_yaml)


async def some_function(
    from_yaml: Instruction,
    from_pedecessor: TaskOutput,
) -> Result[TaskOutput, str]:
    print("Now, I'm doing something")
    print(from_yaml)
    print(from_pedecessor)
    return Ok(TaskOutput(data={"template_task": "TemplateTask is running"}))
