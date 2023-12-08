import sys
import math
from dataclasses import dataclass

@dataclass
class Node:
    label: str
    left: str
    right: str

def read_input(input: str):
    with open(input) as f:
        text = f.read().strip()
        step_pattern, instructions_block = text.split("\n\n")
    lines = instructions_block.split("\n")
    nodes = {}
    for line in lines:
        label, adj_labels = [x.strip() for x in line.split("=")]
        left_label, right_label = [x.strip() for x in adj_labels.split(",")]
        left_label = left_label[1:]
        right_label = right_label[:-1]
        nodes[label] = Node(label, left_label, right_label)
    return step_pattern, nodes

def find_destination_for_current_node(label, nodes, pattern):
    """find destination of a node after following the step pattern"""
    curr_node = nodes[label]
    for step in pattern:
        if step == "L":
            curr_node = nodes[curr_node.left]
        else:
            curr_node = nodes[curr_node.right]
    return curr_node.label

def find_destination_for_all_nodes(nodes, pattern):
    """find destination of each nodes after following the step pattern"""
    destinations = {}
    for label in nodes.keys():
        destination = find_destination_for_current_node(label, nodes, pattern)
        destinations[label] = destination
    return destinations

def count_cycles(destinations, start, end_nodes):
    """
    Count the number of cycles required to reach any end node
    given the start node
    """
    cycles = 0
    curr_label = start
    while not curr_label in end_nodes:
        curr_label = destinations[curr_label]
        cycles += 1
    return cycles

def find_terminal_nodes(nodes, target):
    """find nodes whose labels end with target"""
    start_nodes = set()
    for label in nodes.keys():
        if label[-1] == target:
            start_nodes.add(label)
    return start_nodes

def find_end_nodes(nodes):
    """End nodes end with Z"""
    return find_terminal_nodes(nodes, "Z")

def find_start_nodes(nodes):
    """Start nodes end with A"""
    return find_terminal_nodes(nodes, "A")

def count_steps_for_ghosts(nodes, pattern, destinations):
    """
    count the number of steps needed to reach a destination
    for each node. the soonest that the ghost can simultaneously
    occupy only end nodes (those that end with "Z") is the
    least common multiple of these values.
    """
    start_nodes = find_start_nodes(nodes)
    end_nodes = find_end_nodes(nodes)
    steps = []
    for label in start_nodes:
        cycles = count_cycles(destinations, label, end_nodes)
        steps.append(cycles * len(pattern))
    return compute_lcm(steps)

def compute_lcm(values):
    lcm = 1
    for num in values:
        lcm = lcm * num // math.gcd(lcm,num)
    return lcm

if __name__ == "__main__":
    pattern, nodes = read_input(sys.argv[1])
    destinations = find_destination_for_all_nodes(nodes, pattern)
    steps = count_cycles(destinations, "AAA", {"ZZZ"}) * len(pattern)
    print(steps)

    steps_for_ghosts = count_steps_for_ghosts(nodes, pattern, destinations)
    print(steps_for_ghosts)
