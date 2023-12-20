import math
import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union

class Pulse(Enum):
    LOW = 0
    HIGH = 1

@dataclass
class Action:
    sender: str
    receiver: str
    pulse: Pulse

class FlipFlop:

    def __init__(self, name: str, outputs: List[str], is_on: bool = False):
        self.name = name
        self.outputs = outputs
        self.is_on = is_on

    def process_pulse(self, pulse: Pulse) -> List[Action]:
        if pulse is Pulse.HIGH:
            return []
        self.is_on = not self.is_on
        pulse_to_send = Pulse.HIGH if self.is_on else Pulse.LOW
        actions = []
        for output in self.outputs:
            actions.append(Action(self.name, output, pulse_to_send))
        return actions

class Broadcast:

    def __init__(self, outputs: List[str], name: str = "broadcaster"):
        self.name = name
        self.outputs = outputs

    def process_pulse(self, pulse: Pulse) -> List[Action]:
        actions = []
        for output in self.outputs:
            actions.append(Action(self.name, output, pulse))
        return actions

class Conjunction:

    def __init__(self, name: str, inputs: List[str], outputs: List[str]):
        self.name = name
        self.outputs = outputs
        self.input_memory = {}
        for input in inputs:
            self.input_memory[input] = Pulse.LOW

    def process_pulse(self, input: str, pulse: Pulse) -> List[Action]:
        self.input_memory[input] = pulse
        if all([x == Pulse.HIGH for x in self.input_memory.values()]):
            pulse_to_send = Pulse.LOW
        else:
            pulse_to_send = Pulse.HIGH
        actions = []
        for output in self.outputs:
            actions.append(Action(self.name, output, pulse_to_send))
        return actions

def read_input(filename: str) -> Tuple[Dict[str, str], Dict[str, str], List[str], List[str]]:

    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    module_inputs = {}
    module_outputs = {}
    flipflops = []
    conjunctions = []
    for line in lines:
        input, outputs = line.split(" -> ")
        outputs = [x.strip() for x in outputs.split(",")]
        if input == "broadcaster":
            module_outputs[input] = outputs
            module_inputs[input] = []
        else:
            symbol = input[0]
            input = input[1:]
            if symbol == "%":
                flipflops.append(input)
            elif symbol == "&":
                conjunctions.append(input)
            module_outputs[input] = outputs
        for out in outputs:
            if out not in module_inputs:
                module_inputs[out] = []
            module_inputs[out].append(input)

    return module_inputs, module_outputs, flipflops, conjunctions

def build_modules(
        module_inputs: Dict[str, str],
        module_outputs: Dict[str, str],
        flipflops: List[str],
        conjunctions: List[str]) -> Dict[str, Union[FlipFlop, Broadcast, Conjunction]]:

    labels2modules = {}
    for name in flipflops:
        module = FlipFlop(name, module_outputs[name])
        labels2modules[name] = module
    for name in conjunctions:
        module = Conjunction(name, module_inputs[name], module_outputs[name])
        labels2modules[name] = module
    labels2modules["broadcaster"] = Broadcast(module_outputs["broadcaster"])
    
    return labels2modules

def push_button(
        modules: Dict[str, Union[FlipFlop, Broadcast, Conjunction]],
        target: Action = None) -> Optional[Dict[Pulse, int]]:
    """
    Pushes the button module to send a low pulse to the broadcaster.
    A pulse travels from the broadcaster to all of its destination
    modules in the first time step. The pulse is then propagated from
    those modules in the next time step. This is done using a queue,
    where the queue is emptied for each time step and replenished
    for the next time step until the pulses reach their final destination.
    If the final destination is reached, return the number of 
    low and high pulses sent throughout the process.

    An option to provide a target action allows for detection of
    an event in which a module sends a specific pulse to a specific
    target. Short circuit and return None when the target is found.
    """
    queue = Queue()
    # this is the action performed by the initial button press
    initial_push = Action("button", "broadcaster", Pulse.LOW)
    queue.put(initial_push)
    pulse_counts = {
        Pulse.LOW: 1, # count the initial low pulse here
        Pulse.HIGH: 0,
    }
    while not queue.empty():
        # process all actions at this time step and
        # queue up actions for the next time step
        n_actions = queue.qsize()
        for _ in range(n_actions):
            action = queue.get()
            # find target flipflop and check if it got turned on
            if target is not None:
                if action == target:
                    return None
            # pulse went to a test module
            if not action.receiver in modules:
                continue
            receiver = modules[action.receiver]
            if isinstance(receiver, Conjunction):
                new_actions = receiver.process_pulse(action.sender, action.pulse)
            else:
                new_actions = receiver.process_pulse(action.pulse)
            for new_action in new_actions:
                pulse_counts[new_action.pulse] += 1
                queue.put(new_action)
    return pulse_counts

def push_button_n_times(
        modules: Dict[str, Union[FlipFlop, Broadcast, Conjunction]],
        n: int) -> Dict[Pulse, int]:
    """
    Get low and high pulse counts after n button presses,
    with memory of the module states retained following
    each button press.
    """
    pulse_counts = {
        Pulse.LOW: 0,
        Pulse.HIGH: 0,
    }
    for _ in range(n):
        counts = push_button(modules)
        for key in counts:
            pulse_counts[key] += counts[key]
    return pulse_counts

def push_button_until_target(
        modules: Dict[str, Union[FlipFlop, Broadcast, Conjunction]],
        target: Action) -> int:
    """
    Push the button until a target action is detected.
    Return the number of button presses required to
    reach that target.
    """
    count = 0
    stop_when_none = False
    while stop_when_none is not None:
        stop_when_none = push_button(modules, target)
        count += 1
    return count

def push_button_until_rx_is_on(
        info_from_input: Tuple[Dict[str, str], Dict[str, str], List[str], List[str]]) -> int:
    """
    Manually inspecting the input document shows that the
    "kz" Conjunction module is the only one that sends a 
    signal to module "rx". It will take many button presses
    for this to happen, but it can be observed that Conjunctions
    "sj", "qq", "ls", and "bg" are inputs to "kz". When
    each of those conjunctions sends a HIGH pulse to "kz", 
    "kz" will in turn send a LOW signal to "rx", which will
    turn "rx" on.

    To speed up this process, we search for when "sj", "qq",
    "ls", and "bg" separately send a HIGH pulse to "kz" for
    the first time. Taking the least common multiple then tells
    us when these cycles converge to send HIGH pulses to "kz"
    within the same button press.
    """
    targets = [Action("sj", "kz", Pulse.HIGH),
               Action("qq", "kz", Pulse.HIGH),
               Action("ls", "kz", Pulse.HIGH),
               Action("bg", "kz", Pulse.HIGH),
    ]
    presses_until_on = []
    for target in targets:
        modules = build_modules(*info_from_input)
        presses = push_button_until_target(modules, target)
        presses_until_on.append(presses)
    num_presses = compute_lcm(presses_until_on)
    return num_presses

def compute_lcm(values: List[int]) -> int:
    lcm = 1
    for num in values:
        lcm = lcm * num // math.gcd(lcm, num)
    return lcm

if __name__ == "__main__":
    info_from_input = read_input(sys.argv[1])
    modules = build_modules(*info_from_input)
    # counts = push_button(modules)
    counts = push_button_n_times(modules, 1000)
    print(counts[Pulse.LOW] * counts[Pulse.HIGH])

    num_button_presses = push_button_until_rx_is_on(info_from_input)
    print(num_button_presses)