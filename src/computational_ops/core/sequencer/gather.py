from pathlib import Path
from typing import TYPE_CHECKING

from computational_ops.core.instruction import Instruction
from computational_ops.core.result import Err, Ok, Result
from computational_ops.core.task.loader import LoadedTask, load_tasks

if TYPE_CHECKING:
    from computational_ops.core.task import Task

from .sequence import PipelineSequence


class PipelineGather:
    """PipelineGather is a class that gathers the tasks from the yaml file.

    Args:
        from_yaml (Instruction): The instruction to run the task.
    """

    tasks_candidates: list[LoadedTask] = []
    tasks_names: list[str] = []

    def __init__(self, tasks_path: Path) -> None:
        self.tasks_path = tasks_path

    async def load_tasks(self) -> Result[list[LoadedTask], str]:
        self.tasks_candidates = await load_tasks(self.tasks_path)
        if not self.tasks_candidates:
            return Err("No tasks found")
        self.tasks_names = [task.class_name for task in self.tasks_candidates]
        return Ok(self.tasks_candidates)

    def get_tasks(self, from_yaml: list[Instruction]) -> Result[PipelineSequence, str]:
        # No tasks to run in the yaml file.
        if len(from_yaml) == 0:
            return Err("No tasks found")
        # Load the tasks along with the yaml file.
        tasks: list[Task] = []
        for instruction in from_yaml:
            if instruction.task_name not in self.tasks_names:
                return Err(f"Task {instruction.task_name} not found")
            task_candidate = self.tasks_candidates[self.tasks_names.index(instruction.task_name)]
            tasks.append(
                task_candidate.class_object(
                    name=instruction.task_name,
                    from_yaml=instruction,
                ),
            )
        return Ok(PipelineSequence(tasks=tasks))
