from dataclasses import dataclass
from pathlib import Path
from typing import Any

from yaml import safe_load  # type: ignore[no-untyped-call]

from computational_ops.core.result import Err, Ok, Result, result


@dataclass
class Instruction:
    """Instruction

    A class that represents an instruction for each task.

    Attributes:
        task_name (str): The name of the task.
        task_args (dict[str, Any]): The arguments for the task.
    """

    task_name: str
    task_args: dict[str, Any]


@result
def load_instructions(filepath: Path) -> Result[list[Instruction], TypeError]:
    data = typed_data(filepath).unwrap()
    return Ok(
        [Instruction(name, item) for name, item in data.items()],
    )


@result
def typed_data(filepath: Path) -> Result[dict[str, dict[str, Any]], TypeError]:
    with filepath.open() as file:
        data = safe_load(file)  # type: ignore[no-untyped-call]

    if data is None:
        msg = f"Invalid instructions file: {filepath}\n\t"
        msg += "The file is empty or not a valid YAML file."
        return Err(TypeError(msg))
    if isinstance(data, list):
        msg = f"Invalid instructions file: {filepath}\n\t"
        msg += "The first element of the file is a list, not a dictionary."
        return Err(TypeError(msg))
    if not isinstance(data, dict):
        unknown_type: str = f"{type(data)}"  # type: ignore[attr-defined]
        msg = f"Invalid instructions file: {filepath}\n\t"
        msg += f"The first element of the file is not a dictionary, {unknown_type}."
        return Err(TypeError(msg))
    for name, item in data.items():  # type: ignore[attr-defined]
        if not isinstance(name, str):
            msg = f"Invalid instructions file: {filepath}\n\t"
            msg += "The key of the first element of the file is not a string."
            return Err(TypeError(msg))
        if not isinstance(item, dict):
            msg = f"Invalid instructions file: {filepath}\n\t"
            msg += "The value of the second element of the file is not a dictionary."
            return Err(TypeError(msg))
        for key in item:  # type: ignore[attr-defined]
            if not isinstance(key, str):
                msg = f"Invalid instructions file: {filepath}\n\t"
                msg += "The key of the second element of the file is not a string."
                return Err(TypeError(msg))

    # type: ignore[no-redef]
    checked_data: dict[str, dict[str, Any]] = data

    return Ok(checked_data)
