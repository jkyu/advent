import sys

from dataclasses import dataclass

def read_input(file):
    with open(file, "r") as f:
        grid = f.read().strip().splitlines()
    return grid

@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def __add__(self, other):
        return Coordinate(
            self.row + other.row,
            self.col + other.col,
        )

def find_lit_lights(grid):
    lit_lights = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "#":
                lit_lights.add(Coordinate(row, col))
    return lit_lights

def is_valid(coordinate, row_limit, col_limit):
    if coordinate.row < 0 or coordinate.row >= row_limit:
        return False
    if coordinate.col < 0 or coordinate.col >= col_limit:
        return False
    return True

def propagate(lit_lights, row_limit, col_limit):
    """
    Propagation occurs by looking only at the lit lights at each
    iteration. Neighbors of each lit light will potentially need
    updates. For example, if the same light shows up as a neighbor
    of two or three lit lights, it may need to be turned on.
    
    This should perform better than brute force iteration over
    the light grid because we only check the neighbors of lit
    lights, as opposed to checking the neighbors of every light
    in the grid. If every light in the grid is on, this will
    behave the same as in the brute force case.
    """
    directions = [
        (1, 0), (1, 1), (1, -1), (0, 1),
        (-1, 0), (-1, -1), (-1, 1), (0, -1),
    ]
    directions = [Coordinate(*pair) for pair in directions]
    light_updates = {}
    for light in lit_lights:
        # potentially update any light that is on
        # this catches the case where a light does 
        # not have any neighbors that are on
        if not light in light_updates:
            light_updates[light] = 0
        # increment count for each of a lit light's neighbors
        # each neighbor is a light that potentiall needs updating
        for direction in directions:
            neighbor = light + direction
            if not is_valid(neighbor, row_limit, col_limit):
                continue
            light_updates[neighbor] = light_updates.get(neighbor, 0) + 1

    # for all update candidates, apply light switch logic
    for light, count in light_updates.items():
        # an already lit light will turn off if it does not have
        # two or three lit neighbors
        if light in lit_lights:
            if not count in {2, 3}:
                lit_lights.remove(light)
        # a light that are not already lit will turn off if
        # has exactly three lit neighbors
        else:
            if count == 3:
                lit_lights.add(light)
    return lit_lights

def count_lit_lights_after_n_steps(grid, n, corners_on=False):
    """
    Gather lit lights. Potentially enforce the corners to be on.
    Then propagate the lit lights over time for n time steps.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    lit_lights = find_lit_lights(grid)
    corners = {
        Coordinate(0, 0),
        Coordinate(n_rows-1, 0),
        Coordinate(0, n_cols-1),
        Coordinate(n_rows-1, n_cols-1),
    }
    if corners_on:
        lit_lights.update(corners)
    for _ in range(n):
        lit_lights = propagate(lit_lights, n_rows, n_cols)
        if corners_on:
            lit_lights.update(corners)
    return len(lit_lights)

if __name__ == "__main__":
    grid = read_input(sys.argv[1])
    n_lit_lights = count_lit_lights_after_n_steps(grid, 100)
    print(n_lit_lights)

    n_lit_lights = count_lit_lights_after_n_steps(grid, 100, True)
    print(n_lit_lights)
