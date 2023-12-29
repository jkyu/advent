import re
import sys

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Set

class Gate(Enum):
    AND = "AND"
    OR = "OR"
    LSHIFT = "LSHIFT"
    RSHIFT = "RSHIFT"
    NOT = "NOT"

    @classmethod
    def from_string(cls, string):
        match string:
            case cls.AND.value:
                return cls.AND
            case cls.OR.value:
                return cls.OR
            case cls.LSHIFT.value:
                return cls.LSHIFT
            case cls.RSHIFT.value:
                return cls.RSHIFT
            case cls.NOT.value:
                return cls.NOT

@dataclass
class Wire:
    name: str = None
    signal: int = None

    def __hash__(self):
        return hash(self.name)

@dataclass
class Connector:
    gate: Gate
    incoming: List[Wire]
    outgoing: Wire
    shift: int = None
    done: bool = False

    @property
    def is_ready(self):
        """
        Check if the connector's incoming wires all
        have signal. A connector cannot apply its gate
        twice, so return false if the connector is "done".
        """
        if self.done:
            return False
        for wire in self.incoming:
            if wire.signal is None:
                return False
        return True

    def send_signal_to_outputs(self):
        """Pass the signal to the destination wire."""
        signal = self.get_signal()
        self.outgoing.signal = signal
        self.done = True

    def get_signal(self):
        """Perform gate operation based on gate type"""
        match self.gate:
            case Gate.AND:
                return self.incoming[0].signal & self.incoming[1].signal
            case Gate.OR:
                return self.incoming[0].signal | self.incoming[1].signal
            case Gate.LSHIFT:
                return self.incoming[0].signal << self.shift
            case Gate.RSHIFT:
                return self.incoming[0].signal >> self.shift
            case Gate.NOT:
                # need 16-bit bitmask
                return ~self.incoming[0].signal & 0xFFFF
            case None:
                return self.incoming[0].signal

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    return lines

def set_up_wires(instructions):
    wires = {}
    for line in instructions:
        names = re.findall(r'[a-z]+', line)
        for name in names:
            wires[name] = Wire(name)
    return wires

def set_up_connectors(instructions, wires):
    """
    Link input wires, gates, and output wires through "Connector"
    objects. This will set up a topological sort that will let us
    process Connectors whose input wires have signals and are
    ready to be processed through the gate.
    """
    connectors = []
    for line in instructions:
        inputs, output = [x.strip() for x in line.split("->")]
        output_wire = wires[output]
        try: 
            # wires that will have signals at the first time step
            signal = int(inputs)
            output_wire.signal = signal
        except:
            try:
                gate = Gate.from_string(re.findall(r'[A-Z]+', inputs)[0])
            except:
                gate = None
            match gate:
                case Gate.AND | Gate.OR:
                    input_names = re.findall(r'[a-z]+', inputs)
                    input_wires = [wires[name] for name in input_names]
                    signals = re.findall(r'[0-9]+', inputs)
                    # make one-off wires that we don't need to store
                    # to handle case where a signal comes in not from a wire
                    input_wires += [Wire(signal=int(signal)) for signal in signals]
                    connector = Connector(gate, input_wires, output_wire)
                case Gate.LSHIFT | Gate.RSHIFT:
                    shift = int(re.findall(r'[0-9]+', inputs)[0])
                    name = re.findall(r'[a-z]+', inputs)[0]
                    connector = Connector(gate, [wires[name]], output_wire, shift) 
                case Gate.NOT:
                    name = re.findall(r'[a-z]+', inputs)[0]
                    connector = Connector(gate, [wires[name]], output_wire)
                case None:
                    name = re.findall(r'[a-z]+', inputs)[0]
                    connector = Connector(gate, [wires[name]], output_wire)
            connectors.append(connector)
    return connectors

def propagate_signals(connectors):
    """
    Topological sort on connectors that are ready.
    Once a connector's input wires all have signals,
    it will apply its gate operation and send the
    new signal to its destination wire. A connector
    is not allowed to fire twice.

    This continues until a time step at which no
    connectors are processed.
    """
    done = False
    while not done:
        done = True
        for connector in connectors:
            if connector.is_ready:
                connector.send_signal_to_outputs()
                done = False

if __name__ == "__main__":
    instructions = read_input(sys.argv[1])
    wires = set_up_wires(instructions)
    connectors = set_up_connectors(instructions, wires)
    propagate_signals(connectors)
    wire_a_signal = wires["a"].signal
    print(wire_a_signal)

    wires = set_up_wires(instructions)
    connectors = set_up_connectors(instructions, wires)
    wires["b"].signal = wire_a_signal
    propagate_signals(connectors)
    wire_a_signal = wires["a"].signal
    print(wire_a_signal)
