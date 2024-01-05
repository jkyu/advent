import sys

from dataclasses import dataclass
from typing import Dict, List


class Location:
    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name
        self.next_stops = {}

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Location({self.name})"


@dataclass
class State:
    current_location: Location
    visited_status: int

    def __hash__(self):
        return hash((self.current_location, self.visited_status))


def read_input(file: str) -> List[Location]:
    """
    Build a bidirectional graph of locations with edge
    weights as the distance between the two locations.
    For each location, assign a unique index, which
    will serve as a bitmask.
    """
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    index = 0
    location_map = {}
    for line in lines:
        line = line.split()
        start = line[0]
        if start not in location_map:
            location_map[start] = Location(1 << index, start)
            index += 1
        start_location = location_map[start]
        end = line[2]
        if end not in location_map:
            location_map[end] = Location(1 << index, end)
            index += 1
        end_location = location_map[end]
        distance = int(line[4])
        start_location.next_stops[end_location] = distance
        end_location.next_stops[start_location] = distance
    return list(location_map.values())


def find_best_path(
        location: Location,
        visited: int,
        limit: int,
        cache: Dict[State, int],
        longest: bool,
) -> int:
    """
    Depth-first search with memoization to find the longest or
    shortest path length. The state of the problem is the current
    location and a record of the locations that have already been
    visited. The visited locations are tracked bitwise in an integer
    "visited", so that the & a location's index reveals whether it
    has already been visited.
    """
    # stop when we have visited all of the locations
    if visited == limit:
        return 0

    # check whether state has been evaluated before
    state = State(location, visited)
    if state in cache:
        return cache[state]

    if longest:
        optimal_distance = -sys.maxsize
    else:
        optimal_distance = sys.maxsize

    # attempt to travel to next location
    for next_stop, distance in location.next_stops.items():
        # do not revisit locations
        if next_stop.index & visited:
            continue
        visited = visited | next_stop.index
        remaining_distance = find_best_path(
            next_stop,
            visited,
            limit,
            cache,
            longest,
        )
        # backtrack
        visited = visited ^ next_stop.index
        total_distance = distance + remaining_distance
        if longest:
            optimal_distance = max(total_distance, optimal_distance)
        else:
            optimal_distance = min(total_distance, optimal_distance)

    # cache result for state
    cache[state] = optimal_distance
    return optimal_distance


def find_shortest_path(locations: List[Location]) -> int:
    """
    Find the shortest path through all locations taking
    each location as a starting point.
    """
    shortest = sys.maxsize
    limit = 0
    for i in range(len(locations)):
        limit = limit | 1 << i
    cache = {}
    for start in locations:
        visited = start.index
        best_length = find_best_path(
            start,
            visited,
            limit,
            cache,
            False,
        )
        shortest = min(shortest, best_length)
    return shortest


def find_longest_path(locations: List[Location]) -> int:
    """
    Find the longest path through all locations taking
    each location as a starting point.
    """
    longest = -sys.maxsize
    limit = 0
    for i in range(len(locations)):
        limit = limit | 1 << i
    cache = {}
    for start in locations:
        visited = start.index
        best_length = find_best_path(
            start,
            visited,
            limit,
            cache,
            True,
        )
        longest = max(longest, best_length)
    return longest


if __name__ == "__main__":
    locations = read_input(sys.argv[1])
    print(find_shortest_path(locations))
    print(find_longest_path(locations))
