import sys

from queue import Queue
from typing import List

def read_input(filename: str) -> List[str]:

    with open(filename, "r") as f:
        grid = f.read().strip().splitlines()
    return [list(line) for line in grid]

def bfs(grid, step_limit):
    """
    Use standard breadth-first search to find plots that can
    be reached. The plots we can stop at are determined by
    the step limit. If the step limit is odd, we can only finish
    an odd number of steps away from the starting point. If the
    step limit is even, we can only finish an even number of steps
    away from the starting point. So keep track of garden plots
    that are an odd/even number of steps away from the starting
    point depending on the step limit and keep going until the 
    search runs out of possible steps.
    """
    size = len(grid)
    start_row, start_col = size//2, size//2
    queue = Queue()
    queue.put((start_row, start_col))
    steps = 0
    visited = set()
    directions = [(1,0), (0,1), (0,-1), (-1,0)]
    reachable_plots = set()
    while steps <= step_limit:
        for _ in range(queue.qsize()):
            row, col = queue.get()
            if steps % 2 == step_limit % 2:
                reachable_plots.add((row, col))
            for drow, dcol in directions:
                new_row = row + drow
                new_col = col + dcol
                coords = (new_row, new_col)
                if 0 <= new_row < size and 0 <= new_col < size:
                    if not coords in visited and grid[new_row][new_col] in {".", "S"}:
                        visited.add(coords)
                        queue.put(coords)
        steps += 1
    return reachable_plots

def find_start(grid):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                return (row, col)

def make_super_grid(grid, repeats):
    """
    Stack the grid to make it repeat vertically and horizontally.
    """
    super_grid = []
    for row in grid:
        super_grid.append(row*repeats)
    return super_grid*repeats

def lagrange_interpolation(y0, y1, y2, x):
    """
    Worked out interpolation for a second-order polynomial
    using Lagrange interpolation:
    p(x) = a2 * x^2 + a1 * x + a0

    ref: https://en.wikipedia.org/wiki/Polynomial_interpolation#Lagrange_Interpolation
    """
    # first order coefficient
    a1 = -y0 + 2*y1 - y2/2
    # second order coefficient
    a2 = y0/2 - y1 + y2/2
    estimate = y0 + a1*x + a2 * x**2
    return estimate

if __name__ == "__main__":
    grid = read_input(sys.argv[1])
    size = len(grid)
    reachable_plots = bfs(grid, 64)
    print(len(reachable_plots))

    """
    The grid has a perfect diamond shape where there are no obstables.
    Since the BFS grows in four directions, this is the kind of shape
    it would take if there were no obstacles, and the area of the
    diamond would grow quadratically. Notice that target % size = 65.
    If we take 65 + n*size steps, we see a quadratic increase in the
    number of reachable garden plots. As a result, every grid worth
    of steps (size) repeats the pattern quadratically.

    Fit a polynomial f(n) = y such to predict the number of reachable
    plots at the target number of steps.

    The actual numbers for the fit are:
    n = 0, y = 3752
    n = 1, y = 33614
    n = 2, y = 93252
    """
    target = 26501365
    # have to make the grid big enough to support
    # traveling out farther than one grid size.
    super_grid = make_super_grid(grid, 9)
    y0 = len(bfs(super_grid, target%size))
    y1 = len(bfs(super_grid, target%size+size))
    y2 = len(bfs(super_grid, target%size+2*size))
    print(y0, y1, y2)
    print(lagrange_interpolation(y0, y1, y2, 26501365//131))
