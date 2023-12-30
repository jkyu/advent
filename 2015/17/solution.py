import sys

from dataclasses import dataclass
from typing import Dict, List

def read_input(file: str) -> List[int]:
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    return [int(line) for line in lines]

@dataclass(frozen=True)
class State:
    index: int
    liters_left: int
    container_count: int = None

    def __hash__(self):
        return hash((self.index, self.liters_left, self.container_count))

@dataclass(frozen=True)
class CombinationCount:
    n_combinations: int
    containers_needed: int

    def __add__(self, other):
        return CombinationCount(
            self.n_combinations + other.n_combinations,
            min(self.containers_needed, other.containers_needed),
        )

def fill_container(
        containers: List[int],
        container_number: int,
        liters_left: int,
        containers_used: int,
        cache: Dict[State, CombinationCount],
    ) -> CombinationCount:
    """
    Find number of ways to fill the containers such that
    each container used is completely filled.
    At the same time, try to discover the minimum number
    of containers needed to hold all of the eggnog.
    """
    # base case 1: filled perfectly. accept combination.
    if liters_left == 0:
        return CombinationCount(1, containers_used)
    # base case 2: overfilled. reject combination.
    if liters_left < 0:
        return CombinationCount(0, sys.maxsize)
    # base case 3: out of containers. reject combination.
    if container_number == len(containers):
        return CombinationCount(0, sys.maxsize)

    # if already have result in cache, skip computation
    state = State(container_number, liters_left)
    if state in cache:
        return cache[state]
    
    # try to fill this container
    fill = fill_container(
        containers,
        container_number + 1,
        liters_left - containers[container_number],
        containers_used + 1,
        cache,
    )
    # or skip this container
    skip = fill_container(
        containers,
        container_number + 1,
        liters_left,
        containers_used,
        cache,
    )

    # number of valid combinations is the number of
    # successful ways to perfectly fill containers
    # either filling or skipping this container
    combination_count = fill + skip
    cache[state] = combination_count
    return combination_count


def fill_container_with_limit(
        containers: List[int],
        container_number: int,
        liters_left: int,
        containers_used: int,
        container_limit: int,
        cache: Dict[State, int],
    ) -> int:
    """
    Find number of ways to fill the containers such that
    each container used is completely filled under the
    additional constraint that only a limited number
    of containers can be used.
    """
    # base case 1: used as many containers as allowed
    if containers_used == container_limit:
        # case 1a: perfectly filled. accept combination.
        if liters_left == 0:
            return 1
        # case 1b: have leftover eggnog but no more containers.
        # reject combination
        else:
            return 0
    # base case 2: overfilled. reject combination.
    if liters_left < 0:
        return 0
    # base case 3: out of containers. reject combination.
    if container_number == len(containers):
        return 0

    # if already have result in cache, skip computation
    state = State(container_number, liters_left, containers_used)
    if state in cache:
        return cache[state]
    
    # try to fill this container
    fill = fill_container_with_limit(
        containers,
        container_number + 1,
        liters_left - containers[container_number],
        containers_used + 1,
        container_limit,
        cache,
    )
    # or skip this container
    skip = fill_container_with_limit(
        containers,
        container_number + 1,
        liters_left,
        containers_used,
        container_limit,
        cache,
    )

    # number of valid combinations is the number of
    # successful ways to perfectly fill containers
    # either filling or skipping this container
    # while satisfying the container limit constraint
    combination_count = fill + skip
    cache[state] = combination_count
    return combination_count


if __name__ == "__main__":
    """
    Solve parts 1 and 2 in two steps.
    The first step finds the minimum number of containers
    required while also counting the number of valid
    container combinations without a container limit.
    The second step then does a search for valid container
    combinations constrained by the limit on containers 
    used that was found in the first step.
    """
    containers = read_input(sys.argv[1])
    combination_count = fill_container(
        containers=containers,
        container_number=0,
        liters_left=150,
        containers_used=0,
        cache=dict(),
    )
    print(combination_count.n_combinations)

    combination_count_with_limit = fill_container_with_limit(
        containers=containers,
        container_number=0,
        liters_left=150,
        containers_used=0,
        container_limit=combination_count.containers_needed,
        cache=dict(),
    )
    print(combination_count_with_limit)
