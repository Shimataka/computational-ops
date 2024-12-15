import unittest
from pathlib import Path

from computational_ops.core.instruction import load_instructions


class TestParsingInstruction(unittest.TestCase):
    def test_parsing_instruction(self) -> None:
        instructions_dirpath = Path(__file__).parents[2].joinpath("test_instructions.yml")
        loaded_instructions = load_instructions(instructions_dirpath)
        assert loaded_instructions.is_ok()
        assert len(loaded_instructions.unwrap()) > 0
        instructions = loaded_instructions.unwrap()
        assert instructions[0].task_name == "Task2"
        assert instructions[0].task_args == {
            "name": "test_01_task_name",
            "variable1": "value1-1",
            "variable2": "value1-2",
        }
        assert instructions[1].task_name == "Task1"
        assert instructions[1].task_args == {
            "name": "test_02_task_name",
            "variable1": "value2-1",
            "variable2": "value2-2",
        }
        assert instructions[2].task_name == "Task3"
        assert instructions[2].task_args == {
            "name": "test_03_task_name",
            "variable1": "value3-1",
            "variable2": "value3-2",
        }


if __name__ == "__main__":
    unittest.main()
