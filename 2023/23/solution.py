import sys

from dataclasses import dataclass
from queue import Queue
from typing import Dict, List, Set, Tuple

sys.setrecursionlimit(10000)

SLOPES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

@dataclass
class Vertex:
    row: int
    col: int

    def __hash__(self):
        return hash(self.coord)

    @property
    def coord(self):
        return (self.row, self.col)

@dataclass
class Edge:
    start: Vertex
    end: Vertex
    length: int

def read_input(input: str) -> List[List[str]]:
    with open(input, "r") as f:
        grid = f.read().strip().splitlines()
    grid = [list(line) for line in grid]
    return grid

def find_path_in_row(grid: List[List[str]], row: int) -> Tuple[int, int]:
    """Use this to find the start or target."""
    for col in range(len(grid[row])):
        if grid[row][col] == ".":
            return (row, col)

def is_valid_path(
        grid: List[List[str]],
        row: int,
        col: int,
        visited: Set[Tuple[int, int]]
    ) -> bool:
    n_rows = len(grid)
    n_cols = len(grid[0])
    return 0 <= row < n_rows and 0 <= col < n_cols and not (row, col) in visited and grid[row][col] != "#"

def find_longest_path(
        grid: List[List[str]],
        target: Tuple[int, int],
        coord: Tuple[int, int],
        visited: Set[Tuple[int, int]],
        path: List[Tuple[int, int]]
    ) -> int:
    """
    Perform depth first search to find the longest path.
    If the current location is on a slope, only one direction
    is available for movement.
    """
    if coord == target:
        return len(path)-1 # don't count the initial tile
    longest = 0
    visited.add(coord)
    if grid[coord[0]][coord[1]] in SLOPES:
        directions = [SLOPES[grid[coord[0]][coord[1]]]]
    else:
        directions = list(SLOPES.values())
    for drow, dcol in directions:
        row = coord[0] + drow
        col = coord[1] + dcol
        new_coord = (row, col)
        if is_valid_path(grid, row, col, visited):
            path.append(new_coord)
            length = find_longest_path(grid, target, new_coord, visited, path)
            longest = max(length, longest)
            path.pop()
    visited.remove(coord)
    return longest

def find_vertices(grid: List[List[str]]) -> Dict[Tuple[int, int], Vertex]:
    """
    Find vertices within the grid. A vertex is a path tile in the grid that
    is adjacent to two or more slopes. In general, this should be any tile which
    presents a fork in the path, but I verified that forks only occur when accompanied
    by adjacent slopes.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    vertices = {}
    for row in range(n_rows):
        for col in range(n_cols):
            if grid[row][col] == "#":
                continue
            n_choices = 0
            for drow, dcol in SLOPES.values():
                new_row = row + drow
                new_col = col + dcol
                if 0 <= new_row < n_rows and 0 <= new_col < n_cols and grid[new_row][new_col] in SLOPES:
                    n_choices += 1
            if n_choices > 1:
                vertices[(row, col)] = Vertex(row, col)
    return vertices

def connect_vertices(
        grid: List[List[str]],
        vertices: Dict[Tuple[int,int], Vertex]
    ) -> Dict[Vertex, List[Edge]]:
    """
    Connect the vertices in the grid and count the edge lengths.
    From each vertex, do breadth first search to find neighboring
    vertices. Store this in a graph.
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    graph = {}
    for start in vertices.values():
        queue = Queue()
        queue.put(start.coord)
        visited = set()
        visited.add(start.coord)
        length = 0
        while not queue.empty():
            for _ in range(queue.qsize()):
                coord = queue.get()
                if coord in vertices and length > 0:
                    if start not in graph:
                        graph[start] = []
                    graph[start].append(Edge(start, vertices[coord], length))
                else:
                    for drow, dcol in SLOPES.values():
                        new_row = coord[0] + drow
                        new_col = coord[1] + dcol
                        if 0 <= new_row < n_rows and 0 <= new_col < n_cols and grid[new_row][new_col] != "#":
                            new_coord = (new_row, new_col)
                            if new_coord not in visited:
                                visited.add(new_coord)
                                queue.put(new_coord)
            length += 1
    return graph

def find_longest_path_through_vertices(
        graph: Dict[Vertex, List[Edge]],
        vertex: Vertex,
        target: Vertex,
        visited: Set[Vertex],
        length: int
    ):
    """Perform DFS on vertices to find the longest path."""
    if vertex == target:
        return length
    visited.add(vertex)
    longest = 0
    for edge in graph[vertex]:
        if edge.end not in visited:
            remaining_length = find_longest_path_through_vertices(
                graph,
                edge.end,
                target,
                visited,
                length+edge.length
            )
            longest = max(remaining_length, longest)
    visited.remove(vertex)
    return longest

if __name__ == "__main__":
    grid = read_input(sys.argv[1])
    start = find_path_in_row(grid, row=0)
    target = find_path_in_row(grid, row=len(grid)-1)
    longest = find_longest_path(grid, target, start, set(), [start])
    print(longest)

    vertices = find_vertices(grid)
    vertices[start] = Vertex(*start)
    vertices[target] = Vertex(*target)
    graph = connect_vertices(grid, vertices)
    longest = find_longest_path_through_vertices(
        graph,
        vertices[start],
        vertices[target],
        set(),
        0
    )
    print(longest)