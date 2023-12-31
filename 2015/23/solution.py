import sys

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

@dataclass
class Register:
    name: str
    value: int = 0

@dataclass(frozen=True)
class Instruction:
    operation: str
    register: Register = None
    offset: int = None

class Operation(Enum):
    HLF = "hlf"
    TPL = "tpl"
    INC = "inc"
    JMP = "jmp"
    JIE = "jie"
    JIO = "jio"

    @classmethod
    def from_string(cls, string):
        return cls[string.upper()]

def hlf(register: Register):
    """Halve the register value"""
    register.value = register.value // 2 

def tpl(register: Register):
    """Triple the register value"""
    register.value = register.value * 3

def inc(register: Register):
    """Increment the register value by 1"""
    register.value += 1

def jmp(offset: int, index: int) -> int:
    """Return the index with an offset"""
    return index + offset

def jie(register: Register, offset: int, index: int) -> int:
    """
    Return index with an offset if the register contains an
    even value. Advance the index otherwise.
    """
    if register.value % 2 == 0:
        return jmp(offset, index)
    return index + 1

def jio(register: Register, offset: int, index: int) -> int:
    """
    Return index with an offset if the register has value
    equal to 1. Advance the index otherwise.
    """
    if register.value == 1:
        return jmp(offset, index)
    return index + 1

def read_instructions(file: str) -> List[Instruction]:
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    instructions = []
    for line in lines:
        components = line.replace(",", "").split()
        operation = Operation.from_string(components[0])
        if operation in {Operation.HLF, Operation.TPL, Operation.INC}:
            instruction = Instruction(
                operation=operation,
                register=components[1],
            )
        elif operation in {Operation.JIE, Operation.JIO}:
            instruction = Instruction(
                operation=operation,
                register=components[1],
                offset=int(components[2]),
            )
        else: # jmp case
            instruction = Instruction(
                operation=operation,
                offset=int(components[1]),
            )
        instructions.append(instruction)
    return instructions

def make_registers(instructions: List[Instruction]) -> Dict[str, Register]:
    registers = {}
    for instruction in instructions:
        if instruction.register is None:
            continue
        if not instruction.register in registers:
            name = instruction.register
            registers[name] = Register(name)
    return registers


def is_valid_instruction(index: int, boundaries: Tuple[int, int]):
    return boundaries[0] <= index <= boundaries[1]

def process_instructions(
        registers: Dict[str, Register],
        instructions: List[Instruction],
    ):
    """
    Process instructions line by line, picking the appropriate
    operation at each line. Some operations will cause the index
    to jump forward or backward and can return to previous operations
    or skip to later operations. 

    Exit the program once the index goes out of bounds, as it
    no longer corresponds to an instruction.
    """
    # start at top of instruction sheet
    index = 0
    boundaries = (0, len(instructions)-1)
    while is_valid_instruction(index, boundaries):
        instruction = instructions[index]
        match instruction.operation:
            case Operation.HLF:
                hlf(registers[instruction.register])
                index += 1
            case Operation.TPL:
                tpl(registers[instruction.register])
                index += 1
            case Operation.INC:
                inc(registers[instruction.register])
                index += 1
            case Operation.JMP:
                index = jmp(
                    instruction.offset,
                    index,
                )
            case Operation.JIE:
                index = jie(
                    registers[instruction.register],
                    instruction.offset,
                    index,
                )
            case Operation.JIO:
                index = jio(
                    registers[instruction.register],
                    instruction.offset,
                    index,
                )

if __name__ == "__main__":
    instructions = read_instructions(sys.argv[1])
    registers = make_registers(instructions)
    process_instructions(registers, instructions)
    print(registers)
    
    # reset registers and set the a register to start at 1
    registers = make_registers(instructions)
    registers["a"].value = 1
    process_instructions(registers, instructions)
    print(registers)
