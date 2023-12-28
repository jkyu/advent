import sys
from enum import Enum
from collections import deque
from dataclasses import dataclass

class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)

DIRECTION_SELECTOR = {
    "-": {
        Direction.NORTH: Direction.NORTH,
        Direction.SOUTH: Direction.SOUTH,
        Direction.WEST: Direction.WEST,
        Direction.EAST: Direction.EAST,
    },
    "|": {
        Direction.NORTH: Direction.NORTH,
        Direction.SOUTH: Direction.SOUTH,
        Direction.WEST: Direction.WEST,
        Direction.EAST: Direction.EAST,
    },
    "L": {
        Direction.SOUTH: Direction.EAST,
        Direction.WEST: Direction.NORTH,
    },
    "J": {
        Direction.SOUTH: Direction.WEST,
        Direction.EAST: Direction.NORTH,
    },
    "7": {
        Direction.NORTH: Direction.WEST,
        Direction.EAST: Direction.SOUTH,
    },
    "F": {
        Direction.NORTH: Direction.EAST,
        Direction.WEST: Direction.SOUTH,
    }
}

@dataclass
class Position:
    row: int
    col: int
    last_direction: Direction = None

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return self.row != other.row or self.col != other.col

def find_farthest_pipe(grid, junk_grid, start_position):
    next_positions = []
    for direction in Direction:
        next_row = start_position.row + direction.value[0]
        next_col = start_position.col + direction.value[1]
        if 0 <= next_row < len(grid) and 0 <= next_col < len(grid[0]):
            next_pipe = grid[next_row][next_col]
            if next_pipe in DIRECTION_SELECTOR and direction in DIRECTION_SELECTOR[next_pipe]:
                next_positions.append(Position(next_row, next_col, direction))
    
    distance = 1
    pos1, pos2 = next_positions
    junk_grid[start_position.row][start_position.col] = False
    junk_grid[pos1.row][pos1.col] = False
    junk_grid[pos2.row][pos2.col] = False
    while pos1 != pos2:
        pos1 = move(grid, pos1)
        pos2 = move(grid, pos2)
        junk_grid[pos1.row][pos1.col] = False
        junk_grid[pos2.row][pos2.col] = False
        distance += 1
    return distance

def move(grid, position):
    current_pipe = grid[position.row][position.col]
    outgoing_direction = DIRECTION_SELECTOR[current_pipe][position.last_direction]
    next_row = position.row + outgoing_direction.value[0]
    next_col = position.col + outgoing_direction.value[1]
    return Position(next_row, next_col, outgoing_direction)

def read_grid(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    grid = [list(line) for line in lines]
    return grid

def find_start_position(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                return Position(row, col)
    return None

def count_enclosed_tiles(grid, junk_grid):
    """
    If the pipe loop is crossed an odd number of times,
    we are inside the loop. If it is crossed an even number
    of times, we are outside the loop.

    Go row by row through the grid and count junk tiles between
    an even crossing until the next odd crossing.
    """
    enclosed = 0
    for row in range(len(grid)):
        crossings = 0
        for col in range(len(grid[row])):
            # LJ is a double crossing. L7 is a single cross.
            # FJ is a single cross. F7 is a double cross.
            # | is a single cross.
            # even crosses wash out, so we only need to count L or J or |
            # to find all odd-numbered crossings.
            if grid[row][col] in "|LJ" and not junk_grid[row][col]:
                crossings += 1
            elif junk_grid[row][col] and crossings%2 == 1:
                enclosed += 1
    return enclosed

if __name__ == "__main__": 
    grid = read_grid(sys.argv[1])
    start_position = find_start_position(grid)
    # track the junk. pipes connected to the starting pipe are not junk.
    # everything else is junk
    junk_grid = [[True]*len(grid[0]) for _ in range(len(grid))]
    distance = find_farthest_pipe(grid, junk_grid, start_position)
    print(distance)

    enclosed = count_enclosed_tiles(grid, junk_grid)
    print(enclosed)