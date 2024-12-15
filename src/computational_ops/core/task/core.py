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

    def __init__(self, name: str, from_yaml: Instruction) -> None:
        """Initialize the task.

        Args:
            name (str): The name of the task.
            from_yaml (Instruction): The instruction to run the task.
        """
        self.name = name
        validated = self.validate_yaml(from_yaml)
        if validated.is_err():
            raise TypeError(validated.unwrap_err())
        self.from_yaml = validated.unwrap()

    @abstractmethod
    def validate_yaml(self, from_yaml: Instruction) -> Result[Instruction, str]:
        """Check the yaml.

        Returns:
            Result[bool, str]: The result of the check.

        Args:
            from_yaml (Instruction): The instruction to run the task.
        """
        raise NotImplementedError

    @abstractmethod
    async def run(self, from_pedecessor: TaskOutput) -> Result[TaskOutput, str]:
        """Run the task.

        Args:
            from_pedecessor (Task): The task that precedes this task.

        Returns:
            Result[TaskOutput, str]: The result of the task.
        """
        raise NotImplementedError
