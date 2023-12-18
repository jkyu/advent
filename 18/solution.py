import sys

from dataclasses import dataclass
from itertools import pairwise
from typing import List

DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

DIRECTION_DECODER = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

@dataclass
class DigInstruction:
    direction: str
    spaces: int

def calculate_perimeter(instructions):
    perimeter = 0
    for instruction in instructions:
        perimeter += instruction.spaces
    return perimeter

def find_vertices(instructions: List[DigInstruction]):
    vertices = [(0,0)]
    for instruction in instructions:
        row, col = vertices[-1]
        new_row = row + instruction.spaces * DIRECTIONS[instruction.direction][0]
        new_col = col + instruction.spaces * DIRECTIONS[instruction.direction][1]
        vertices.append((new_row, new_col))
    return vertices

def shoelace_area(vertices):
    """
    Gauss's (shoelace) area formula to compute trapezoidal
    areas described by pairs of vertices and add/subtract
    the trapezoids to obtain an overall geometric area for
    the polygon described by the set of vertices.

    Note: this implementation assumes that the vertices are
    in counterclockwise order.

    ref: https://en.wikipedia.org/wiki/Shoelace_formula
    """
    area = []
    for (y1, x1), (y2, x2) in pairwise(vertices):
        area.append((y1 + y2) * (x1 - x2))
    area = sum(area) * 0.5
    return area

def calculate_num_interior_points(area, n_boundary):
    """
    Pick's theorem computes the area of a polygon from
    the number of grid points within it and the number of
    points on its boundary: area = n_interior + n_boundary/2 - 1

    Given the area and the number of boundary points,
    the number of grid points enclosed by the polygon
    can be computed: n_interior = area - n_boundary/2 - 1

    ref: https://en.wikipedia.org/wiki/Pick%27s_theorem
    """
    n_interior = area - n_boundary / 2 + 1
    return int(n_interior)

def compute_area(instructions):
    """
    Compute area by finding the vertices and the perimeter
    of the polygon formed by the digging instructions.

    From the list of vertices, use Gauss's (shoelace) area
    formula to compute a geometric area, and then use Pick's
    theorem to compute the number of grid points enclosed by
    the polygon.
    """
    vertices = find_vertices(instructions)
    perimeter = calculate_perimeter(instructions)
    area = shoelace_area(vertices)
    n_interior = calculate_num_interior_points(area, perimeter)
    return perimeter + n_interior

def read_input(input: str) -> List[DigInstruction]:
    with open(input, "r") as f:
        text = f.read().strip().splitlines()
    return text

def process_text_to_instructions(text, decode_hex=False):
    instructions = []
    for line in text:
        direction, spaces, color = line.split()
        if decode_hex:
            # first 5 digits as hex code for spaces to dig
            spaces = int(color[2:-2], 16)
            # last digit encodes the direction
            direction = DIRECTION_DECODER[color[-2]]
        instruction = DigInstruction(direction, int(spaces))
        instructions.append(instruction)
    return instructions

if __name__ == "__main__":
    text = read_input(sys.argv[1])
    instructions = process_text_to_instructions(text)
    area = compute_area(instructions)
    print(area)

    instructions = process_text_to_instructions(text, True)
    area = compute_area(instructions)
    print(area)
