"""Test the core task module.

This module tests the core task module.

TODOS:
    * [ ] Add test for `Instruction` argument.
"""

import unittest

from computational_ops.core.instruction import Instruction
from computational_ops.core.result import Ok, Result
from computational_ops.core.task.core import Task, TaskOutput


class TestTask1(Task):
    async def run(
        self,
        from_yaml: Instruction,  # noqa: ARG002
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        data = from_pedecessor.data
        data["append_on_task1"] = "append_on_task1"
        return Ok(TaskOutput(data=data))


class TestTask2(Task):
    async def run(
        self,
        from_yaml: Instruction,  # noqa: ARG002
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        data = from_pedecessor.data
        data["append_on_task2"] = "append_on_task2"
        return Ok(TaskOutput(data=data))


class TestTask3(Task):
    async def run(
        self,
        from_yaml: Instruction,  # noqa: ARG002
        from_pedecessor: TaskOutput,
    ) -> Result[TaskOutput, str]:
        data = from_pedecessor.data
        data["append_on_task3"] = "append_on_task3"
        return Ok(TaskOutput(data=data))


class TestTask(unittest.IsolatedAsyncioTestCase):
    async def test_task(self) -> None:
        instruction = Instruction(task_name="", task_args={})
        task_a = TestTask1(name="TaskA")
        task_b = TestTask2(name="TaskB")
        task_c = TestTask3(name="TaskC")

        output = await task_a.run(instruction, TaskOutput(data={}))
        output = await task_b.run(instruction, output.unwrap())
        output = await task_c.run(instruction, output.unwrap())

        assert output.unwrap().data == {
            "append_on_task1": "append_on_task1",
            "append_on_task2": "append_on_task2",
            "append_on_task3": "append_on_task3",
        }
