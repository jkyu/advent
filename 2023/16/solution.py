import sys

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import List

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, drow, dcol):
        self.drow = drow
        self.dcol = dcol

    def __hash__(self):
        return hash(self.name)

@dataclass
class State:
    row: int
    col: int
    direction: Direction

    def __hash__(self):
        return hash((self.row, self.col, self.direction))

def read_input(input: str) -> List[List[str]]:
    with open(input, "r") as f:
        grid = f.read().strip().splitlines()
    grid = [list(line) for line in grid]
    return grid

def energize_grid(grid: List[List[str]], start_state: State):
    """
    Use a queue to process each time step for the movement of the beam
    through the grid and track the spaces that become energized.

    Keep track of identical paths taken through the grid to avoid looping.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    active = deque()
    active.append(start_state)
    energized = set()
    seen = set()
    while len(active) > 0:
        for _ in range(len(active)):
            curr_state = active.popleft()
            row = curr_state.row
            col = curr_state.col
            direction = curr_state.direction
            new_row = row + direction.drow
            new_col = col + direction.dcol
            if 0 <= new_row < n_rows and 0 <= new_col < n_cols:
                space = grid[new_row][new_col]
                if space == ".":
                    state = State(new_row, new_col, direction)
                    if state not in seen:
                        active.append(state)
                        seen.add(state)
                        energized.add((new_row, new_col))
                elif space in {"|", "-"}:
                    new_directions = split_beam(direction, space)
                    for new_direction in new_directions:
                        state = State(new_row, new_col, new_direction)
                        if state not in seen:
                            active.append(state)
                            seen.add(state)
                            energized.add((new_row, new_col))
                elif space in {"\\", "/"}:
                    new_direction = reflect_beam(direction, space)
                    state = State(new_row, new_col, new_direction)
                    if state not in seen:
                        active.append(state)
                        seen.add(state)
                        energized.add((new_row, new_col))
                else:
                    raise ValueError("Not a valid space type.")
    return len(energized)

def split_beam(direction, splitter):
    """pick new direction(s) after encountering a splitter"""
    new_directions = []
    if splitter == "|":
        if direction in {Direction.UP, Direction.DOWN}:
            new_directions.append(direction)
        elif direction in {Direction.LEFT, Direction.RIGHT}:
            new_directions.extend([Direction.UP, Direction.DOWN])
        else:
            raise ValueError(f"{direction} is not a valid direction.")
    elif splitter == "-":
        if direction in {Direction.UP, Direction.DOWN}:
            new_directions.extend([Direction.LEFT, Direction.RIGHT])
        elif direction in {Direction.LEFT, Direction.RIGHT}:
            new_directions.append(direction)
        else:
            raise ValueError(f"{direction} is not a valid direction.")
    else:
        raise ValueError(f"{splitter} is not a valid splitter.")
    return new_directions
        
def reflect_beam(direction, mirror):
    """pick new direction after reflecting off a mirror"""
    if mirror == "/":
        if direction == Direction.UP:
            new_direction = Direction.RIGHT
        elif direction == Direction.DOWN:
            new_direction = Direction.LEFT
        elif direction == Direction.RIGHT:
            new_direction = Direction.UP
        elif direction == Direction.LEFT:
            new_direction = Direction.DOWN
        else:
            raise ValueError(f"{direction} is not a valid direction.")
    elif mirror == "\\":
        if direction == Direction.UP:
            new_direction = Direction.LEFT
        elif direction == Direction.DOWN:
            new_direction = Direction.RIGHT
        elif direction == Direction.RIGHT:
            new_direction = Direction.DOWN
        elif direction == Direction.LEFT:
            new_direction = Direction.UP
        else:
            raise ValueError(f"{direction} is not a valid direction.")
    else:
        raise ValueError(f"{mirror} is not a valid mirror.")
    return new_direction

def generate_start_states_from_boundaries(grid) -> List[State]:
    states = []
    n_rows = len(grid)
    n_cols = len(grid[0])
    for row in range(n_rows):
        states.append(State(row, -1, Direction.RIGHT))
        states.append(State(row, n_cols, Direction.LEFT))
    for col in range(n_cols):
        states.append(State(-1, col, Direction.DOWN))
        states.append(State(n_rows, col, Direction.UP))
    return states

def maximize_energized_spaces(grid):
    start_states = generate_start_states_from_boundaries(grid)
    most_energized = -sys.maxsize
    for state in start_states:
        n_energized = energize_grid(grid, state)
        most_energized = max(most_energized, n_energized)
    return most_energized

if __name__ == "__main__":
    grid = read_input(sys.argv[1])
    n_energized = energize_grid(grid, State(0, -1, Direction.RIGHT))
    print(n_energized)
    
    max_energized = maximize_energized_spaces(grid)
    print(max_energized)