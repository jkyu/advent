import re
import sys

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Instruction:
    quantity: int
    source: str
    target: str


class Stacks:

    def __init__(self, names: List[str]):
        self.names = names
        self.stacks = {name: [] for name in names}

    def insert(self, stack_name: str, item: str):
        """Add a crate to the named stack"""
        self.stacks[stack_name].append(item)

    def pop(self, stack_name: str) -> str:
        """Remove a crate from the named stack"""
        return self.stacks[stack_name].pop()

    @property
    def crates_on_top(self) -> str:
        """
        Return a string with the crates currently
        on top of each stack in order.
        """
        on_top = []
        for name in self.names:
            on_top.append(self.stacks[name][-1])
        return "".join(on_top)


def read_input(file_name: str) -> Tuple[str, str]:
    with open(file_name, "r") as f:
        stack_text, instruction_text = f.read().split("\n\n")
    return stack_text, instruction_text


def text_to_instructions(instruction_text: str) -> List[Instruction]:
    instructions = []
    for line in instruction_text.splitlines():
        numbers = re.findall(r'\b[0-9]+\b', line)
        instruction = Instruction(
            int(numbers[0]),
            numbers[1],
            numbers[2],
        )
        instructions.append(instruction)
    return instructions


def text_to_stacks(stack_text: str) -> Stacks:
    stack_lines = stack_text.splitlines()[::-1]
    names_and_indices = []
    names = []
    for i, char in enumerate(stack_lines[0]):
        if char.isnumeric():
            names_and_indices.append((char, i))
            names.append(char)

    stacks = Stacks(names)
    for line in stack_lines[1:]:
        for name, index in names_and_indices:
            if line[index].isalpha():
                stacks.insert(name, line[index])
    return stacks


def process_instructions(
        stacks: Stacks,
        instructions: List[Instruction],
        new_cratemover: bool = False,
):
    for instruction in instructions:
        crates_to_move = []
        for _ in range(instruction.quantity):
            crates_to_move.append(
                stacks.pop(instruction.source)
            )
        # treat crates_to_move as a stack. crates removed
        # from the source stack are placed into the new
        # stack in reverse order
        if new_cratemover:
            while crates_to_move:
                stacks.insert(
                    instruction.target,
                    crates_to_move.pop(),
                )
        # treat crates_to_move as a queue. crates removed
        # from the source stack are placed into the new
        # stack in the same order
        else:
            for crate in crates_to_move:
                stacks.insert(instruction.target, crate)


if __name__ == "__main__":
    cargo_text, procedure_text = read_input(sys.argv[1])
    procedure = text_to_instructions(procedure_text)

    cargo = text_to_stacks(cargo_text)
    process_instructions(cargo, procedure, False)
    print("Part 1:", cargo.crates_on_top)

    # reset the cargo stacks
    cargo = text_to_stacks(cargo_text)
    process_instructions(cargo, procedure, True)
    print("Part 2:", cargo.crates_on_top)
