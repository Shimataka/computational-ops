import asyncio
from argparse import ArgumentParser
from pathlib import Path

from computational_ops.core.instruction import load_instructions
from computational_ops.core.sequencer.gather import PipelineGather
from computational_ops.core.task import TaskOutput


async def main():
    parser = ArgumentParser()
    parser.add_argument("instructions_path", type=Path)
    args = parser.parse_args()
    instructions_path = Path(args.instructions_path)
    instructions = load_instructions(instructions_path)
    if instructions.is_err():
        print(instructions.unwrap_err())
        return
    gather = PipelineGather(Path(__file__).parent.parent / "tasks")
    await gather.load_tasks()
    sequence = gather.get_tasks(instructions.unwrap())
    if sequence.is_err():
        print(sequence.unwrap_err())
        return
    await sequence.unwrap().run(default_output=TaskOutput(data={}))


if __name__ == "__main__":
    asyncio.run(main())
