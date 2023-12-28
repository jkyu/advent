import sys

from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue
from typing import List

MAX_CONSECUTIVE_STEPS = 3
MAX_CONSECUTIVE_STEPS_ULTRA = 10
MIN_CONSECUTIVE_STEPS_ULTRA = 4

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, drow, dcol):
        self.drow = drow
        self.dcol = dcol

    def get_next_direction(self, num_consecutive, ultra_crucible):
        """
        Provide directions that can be taken given the direction
        of rolling that brought the crucible to its current state.
        Restrictions on direction are based on the number of
        consecutive steps in its current direction.

        The crucible can roll no more than max_consecutive_steps
        in a row in the same direction.
        The crucible needs to have rolled a minimum of
        min_consecutive_steps in a row in the same direction
        before it is allowed to turn.
        These values are modulated by whether the crucible is
        a normal one or an ultra crucible.
        """
        moves = []
        if ultra_crucible:
            min_consecutive_steps = MIN_CONSECUTIVE_STEPS_ULTRA
            max_consecutive_steps = MAX_CONSECUTIVE_STEPS_ULTRA
        else:
            min_consecutive_steps = 0
            max_consecutive_steps = MAX_CONSECUTIVE_STEPS
        # straight motion
        if num_consecutive < max_consecutive_steps:
            moves.append(self)
        # turns
        if num_consecutive >= min_consecutive_steps:
            if self in {Direction.UP, Direction.DOWN}:
                moves.append(Direction.LEFT)
                moves.append(Direction.RIGHT)
            elif self in {Direction.LEFT, Direction.RIGHT}:
                moves.append(Direction.UP)
                moves.append(Direction.DOWN)
        return moves

@dataclass
class State:
    heat: int
    row: int
    col: int
    direction: Direction
    n_consecutive: int

    def __lt__(self, other):
        return self.heat < other.heat

def roll_with_least_heat_lost(grid, ultra_crucible=False):
    """
    This is a single source, least expensive path problem.
    So Dijkstra's algorithm solves it.
    Each state details the current heat lost, the coordinates,
    the rolling direction and how long the crucible has rolled
    in that direction.
    For each state, try to go straight or turn right/left and
    then compute the heat lost after having made that move.
    This generates up to three new states that we place back into
    the heap. The heap is ordered strictly by the heat lost
    for each state. This guarantees that the first time the 
    target coordinates are reached will also be the state
    in which the least heat was lost while rolling the crucible
    to the target.

    A flag allows for rolling an ultra crucible instead.
    """
    heap = PriorityQueue()
    heap.put(State(grid[0][1], 0, 1, Direction.RIGHT, 1))
    heap.put(State(grid[1][0], 1, 0, Direction.DOWN, 1))
    visited = set()

    while not heap.empty():
        state = heap.get()
        heat = state.heat
        row = state.row
        col = state.col
        direction = state.direction
        count = state.n_consecutive

        if is_done_rolling(grid, row, col):
            # reached target with minimum heat lost
            return heat

        if (row, col, direction, count) in visited:
            continue
        visited.add((row, col, direction, count))

        for new_direction in direction.get_next_direction(count, ultra_crucible):
            new_row = row + new_direction.drow
            new_col = col + new_direction.dcol
            if is_move_in_bounds(grid, new_row, new_col):
                new_heat = heat + grid[new_row][new_col]
                if direction is new_direction:
                    heap.put(State(new_heat, new_row, new_col, new_direction, count + 1))
                else:
                    heap.put(State(new_heat, new_row, new_col, new_direction, 1))

def is_done_rolling(grid, row, col):
    """reached target (bottom right corner)"""
    return (row == len(grid)-1 and col == len(grid[0])-1)

def is_move_in_bounds(grid, row, col):
    """verify coordinates are within bounds"""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def read_input(input: str) -> List[List[str]]:
    with open(input, "r") as f:
        grid = f.read().strip().splitlines()
    grid = [[int(x) for x in line] for line in grid]
    return grid

if __name__ == "__main__":
    grid = read_input(sys.argv[1])
    heat_lost = roll_with_least_heat_lost(grid)
    print(heat_lost)

    heat_lost = roll_with_least_heat_lost(grid, ultra_crucible=True)
    print(heat_lost)
