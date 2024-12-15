from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from computational_ops.core.instruction import Instruction
from computational_ops.core.result import Result


@dataclass
class TaskOutput:
    """TaskOutput is a class that represents the output of a task.

    Attributes:
        data (dict): The data of the task output.
    """

    data: dict[str, Any]


class Task(ABC):
    """Task is a class that represents a task that can be run.

    Args:
        name (str): The name of the task.

    Returns:
        Result[TaskOutput, str]: The result of the task.
    """

    def __init__(self, name: str) -> None:
        """Initialize the task.

        Args:
            name (str): The name of the task.
        """
        self.name = name

    @abstractmethod
    async def run(
        self,
        from_yaml: Instruction,
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        """Run the task.

        Args:
            from_yaml (Instruction): The instruction to run the task.
            from_pedecessor (Task): The task that precedes this task.

        Returns:
            Result[TaskOutput, str]: The result of the task.
        """
        raise NotImplementedError
