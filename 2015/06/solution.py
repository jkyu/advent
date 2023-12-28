import re
import sys

from dataclasses import dataclass
from enum import Enum, auto

class Action(Enum):
    TOGGLE = "toggle"
    ON = "turn on"
    OFF = "turn off"

@dataclass
class Instruction:
    action: Action
    start_x: int
    start_y: int
    end_x: int
    end_y: int

class Light:
    """
    Keep track of on/off status for regular light bulbs and
    the brightness levels for lightbulbs with brightness
    settings.
    """
    def __init__(self):
        self.on = False
        self.brightness = 0

    def turn_on(self):
        self.on = True
        self.brightness += 1
    
    def turn_off(self):
        self.on = False
        self.brightness -= 1
        self.brightness = max(self.brightness, 0)

    def toggle(self):
        self.on = not self.on
        self.brightness += 2

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    instructions = []
    for line in lines:
        numbers = [int(x) for x in re.findall(r'\d+', line)]
        if line.startswith(Action.TOGGLE.value):
            action = Action.TOGGLE
        elif line.startswith(Action.ON.value):
            action = Action.ON
        else:
            action = Action.OFF
        instruction = Instruction(action, *numbers)
        instructions.append(instruction)
    return instructions

def process_instructions(instructions, start=0, end=1000):
    """
    Brute force: flip/toggle all light switches in the range
    given by each line of instructions.
    """
    lights = {}
    for i in range(start, end):
        for j in range(start, end):
            lights[complex(i, j)] = Light()
    for instruction in instructions:
        for i in range(instruction.start_x, instruction.end_x+1):
            for j in range(instruction.start_y, instruction.end_y+1):
                coordinate = complex(i, j)
                if instruction.action is Action.ON:
                    lights[coordinate].turn_on()
                elif instruction.action is Action.OFF:
                    lights[coordinate].turn_off()
                else:
                    lights[coordinate].toggle()
    return lights

def count_lit_lights(lights):
    return sum([light.on for light in lights.values()])

def sum_light_brightness(lights):
    return sum([light.brightness for light in lights.values()])

if __name__ == "__main__":
    instructions = read_input(sys.argv[1])
    lights = process_instructions(instructions)
    lit_lights = count_lit_lights(lights)
    print(lit_lights)

    brightness = sum_light_brightness(lights)
    print(brightness)
