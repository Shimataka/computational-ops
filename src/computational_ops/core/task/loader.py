import os
from dataclasses import dataclass
from importlib import import_module
from inspect import getmembers, isclass
from pathlib import Path

from .core import Task


@dataclass
class LoadedTask:
    class_name: str
    class_object: type[Task]
    class_path: str


async def get_all_files_in_directory(directory: Path) -> list[LoadedTask]:
    """get_all_files_in_directory

    Args:
        directory (Path): Path to root directory to search for `tasks.py` files.

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing the tasks class name,
        object, and file path.
    """
    loaded_task_list: list[LoadedTask] = []

    # Walk through the directory and lower locations.
    for root, _, files in os.walk(directory):
        print(f">> Searching: {root}")
        for file in files:
            if to_included(root=root, file=file):
                file_name = ".".join(root.split("/")[1:] + [file]).rsplit(".", 1)[0]
                print(f">> Loading task from: {file_name}")
                module = import_module(name=file_name)
                print(f">> Module: {module}")
                for cls_name, cls in getmembers(module, isclass):
                    # print(f">> Loading task: <{cls_name}>")
                    loaded_task_list.append(
                        LoadedTask(
                            class_name=cls_name,
                            class_object=cls,
                            class_path=file_name,
                        ),
                    )
    return loaded_task_list


def to_included(
    root: str,
    file: str,
) -> bool:
    """_to_included

    Decide whether the task is included or not.

    Args:
        root (str): A root directory of these files.
        file (str): The names of the files.

    Returns:
        bool: Whether the task is included or not.
    """
    # Exclusion: template is a file for the task template.
    if "template" in root:
        return False
    # Exclusion: __init__.py is a file without a task.
    if "__init__.py" in file:
        return False
    # Exclusion: this is me.
    if file == Path(__file__).name:
        return False
    # Exclusion: `tasks.py` not included.
    print(f">> To be searched: {Path(root).joinpath(file).as_posix()}")
    return file == "tasks.py"


async def load_tasks(tasks_dirpath: Path) -> list[LoadedTask]:
    """load_tasks

    Load all tasks from the `computational_ops/tasks` directory.

    Args:
        tasks_dirpath (Path): The path to the tasks directory.

    Returns:
        list[LoadedTask]: A list of LoadedTask instances wrapping the loaded task classes.
    """
    loaded_task_list: list[LoadedTask] = []
    # Load all tasks from the tasks directory.
    loaded_task_list = await get_all_files_in_directory(tasks_dirpath)
    for loaded_task in loaded_task_list:
        class_name = loaded_task.class_name
        class_object = loaded_task.class_object
        class_path = loaded_task.class_path
        if class_name:
            loaded_task_list.append(LoadedTask(class_name, class_object, class_path))
    return loaded_task_list
