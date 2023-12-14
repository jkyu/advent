import sys

from enum import Enum

def read_input(input):
    with open(input, "r") as f:
        grid = f.read().strip().splitlines()
    return [list(line) for line in grid]

class Direction(Enum):
    NORTH = (-1, 0)
    WEST = (0, -1)
    SOUTH = (1, 0)
    EAST = (0, 1)

def coordinate_generator(platform, direction):
    n_rows = len(platform)
    n_cols = len(platform[0])
    match(direction):
        case Direction.NORTH | Direction.WEST:
            rows = range(n_rows)
            cols = range(n_cols)
        case Direction.SOUTH:
            rows = range(n_rows-1, -1, -1)
            cols = range(n_cols)
        case Direction.EAST:
            rows = range(n_rows)
            cols = range(n_cols-1, -1, -1)
    for col in cols:
        for row in rows:
            yield row, col

def tilt_platform(platform, direction):
    n_rows = len(platform)
    n_cols = len(platform[0])
    drow, dcol = direction.value
    for row, col in coordinate_generator(platform, direction):
        if platform[row][col] == "O":
            # we're moving this round rock, so empty out the location
            platform[row][col] = "."
            new_row = row
            new_col = col
            # stay in bounds and stop once we hit "#"
            while 0 <= new_row < n_rows and 0 <= new_col < n_cols and platform[new_row][new_col] == ".":
                new_row += drow
                new_col += dcol
            # place round rock at new location but we need to go back one iteration
            platform[new_row - drow][new_col - dcol] = "O"
    return platform

def compute_load(platform):
    """
    A rock at the top of the board has load == n_rows.
    Subtract one from the load for each row away from the top.
    """
    n_rows = len(platform)
    load = 0
    for row in range(len(platform)):
        for rock in platform[row]:
            if rock == "O":
                load += n_rows - row
    return load

def part1(platform):
    platform = tilt_platform(platform, Direction.NORTH)
    return compute_load(platform)

def part2(platform):
    """
    Do tilt cycles until we find a repeat.
    Once we find a repeat, we will repeat the pattern forever.
    Find where 1000000000 lands in that pattern.
    """
    rock_formations = {}
    loads = []
    curr_cycle = 0
    while True:
        curr_cycle += 1
        for direction in Direction:
            platform = tilt_platform(platform, direction)
        load = compute_load(platform)
        loads.append(load)
        formation = "".join(["".join(line) for line in platform])
        if formation in rock_formations:
            cycle_length = curr_cycle - rock_formations[formation]
            # truncate the loads to include only those in the pattern
            cycle_loads = loads[-cycle_length:]
            # find out where 1000000000 lies in the pattern after lopping off
            # the first curr_cycle cycles
            final_index = ((1000000000 - curr_cycle) % cycle_length) - 1
            return cycle_loads[final_index]
        else:
            rock_formations[formation] = curr_cycle
    return -1

if __name__ == "__main__":
    platform = read_input(sys.argv[1])
    load = part1([[rock for rock in line] for line in platform])
    print(load)

    load = part2([[rock for rock in line] for line in platform])
    print(load)