import sys

from typing import List, Set

class Location:
    def __init__(self, name: str):
        self.name = name
        self.next_stops = {}

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Location({self.name})"

def read_input(file: str) -> List[Location]:
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    # build a bidirectional graph of locations
    # with edge weights as the distance between 
    # two locations
    locations = {}
    for line in lines:
        line = line.split()
        start = line[0]
        if start not in locations:
            locations[start] = Location(start)
        start_location = locations[start]
        end = line[2]
        if end not in locations:
            locations[end] = Location(end)
        end_location = locations[end]
        distance = int(line[4])
        # paths are bidirectional
        start_location.next_stops[end_location] = distance
        end_location.next_stops[start_location] = distance
    return list(locations.values())

def find_best_path(
        location: Location,
        visited: Set[Location],
        cumulative_distance: int,
        n_locations: int,
        longest: bool,
    ) -> int:
    """
    Depth-first search to find the longest or shortest path length.
    """
    # stop when we have visited all of the locations
    if len(visited) == n_locations:
        return cumulative_distance
    best_distance = sys.maxsize
    if longest:
        best_distance = -best_distance
    for next_stop, distance in location.next_stops.items():
        # do not revisit locations
        if next_stop in visited:
            continue
        visited.add(next_stop)
        total_distance = find_best_path(
            next_stop,
            visited,
            cumulative_distance + distance,
            n_locations,
            longest,
        )
        visited.remove(next_stop)
        if longest:
            best_distance = max(total_distance, best_distance)
        else:
            best_distance = min(total_distance, best_distance)
    return best_distance

def find_shortest_path(locations: List[Location]) -> int:
    """
    Find the shortest path through all locations taking
    each location as a starting point.
    """
    shortest = sys.maxsize
    for start in locations:
        visited = set()
        visited.add(start)
        best_length = find_best_path(
            start,
            visited,
            0,
            len(locations),
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
    for start in locations:
        visited = set()
        visited.add(start)
        best_length = find_best_path(
            start,
            visited,
            0,
            len(locations),
            True,
        )
        longest = max(longest, best_length)
    return longest

if __name__ == "__main__":
    locations = read_input(sys.argv[1])
    print(find_shortest_path(locations))
    print(find_longest_path(locations))
