import sys

from typing import List, Tuple

def read_input(file):
    with open(file, "r") as f:
        numbers = [int(line) for line in f.readlines()]
    return numbers

def find_group1_arrangements(
        weights: List[int],
        index: int,
        group: List[int],
        running_weight: int,
        weight_limit: int,
        present_limit: int,
        candidates: List[Tuple[int, ...]]
    ):
    """
    Depth-first search enumerates possible arrangements for the
    first group. Because the sum of weights for each group must
    be equivalent, the weight of group 1 cannot exceed a limit of
    sum(weights) / n_groups. This is used as a base case:
    a group that exceeds this limit is discarded and a group is
    considered valid if its weight matches the limit exactly.

    The other base cases are running out of presents to add to
    the group and exceeding the number of presents allowed for 
    Group 1. Group 1 is supposed to be the smallest group, so
    there is no case in which it can contain more than 
    len(weights) / n_groups presents. 

    At each index, try to add any one of the remaining presents
    (all presents with smaller indices having already been
    considered). Perform a backtracking search to produce valid
    potential group 1 arrangements.

    Note: there is a big assumption made here that the presents
    not chosen for group 1 can be split into n_groups-1 groups
    that also have weight == sum(weights) / n_groups. This does
    not have to be true, and a general solution would also require
    verifying that the candidate groupings leave presents that
    can be split correctly. The prompt, however, does not require
    consideration of the general case.
    """
    if len(group) > present_limit:
        return
    if running_weight > weight_limit:
        return
    if running_weight == weight_limit:
        candidates.append(tuple(group))
        return
    if index == len(weights):
        return

    for i in range(index, len(weights)):
        group.append(weights[i])
        find_group1_arrangements(
            weights,
            i+1,
            group,
            running_weight + weights[i],
            weight_limit,
            present_limit,
            candidates,
        )
        group.pop()

def compute_entanglement(group: Tuple[int, ...]) -> int:
    product = 1
    for weight in group:
        product *= weight
    return product

def find_best_group1_arrangement(
        weights: List[int],
        n_groups: int
    ) -> int:
    """
    Find the smallest group with the lowest entanglement, given a
    list of weights for each present and the number of groups into
    which to split the presents.
    """
    weight_limit = sum(weights) // n_groups
    size_limit = len(weights) // n_groups
    candidates = []
    find_group1_arrangements(
        weights, 0, [], 0, weight_limit, size_limit, candidates
    )

    smallest = len(weights)
    min_entanglement = sys.maxsize
    for group in candidates:
        if len(group) > smallest:
            continue
        elif len(group) < smallest:
            smallest = len(group)
            min_entanglement = compute_entanglement(group)
        else:
            entanglement = compute_entanglement(group)
            min_entanglement = min(min_entanglement, entanglement)

    return min_entanglement

if __name__ == "__main__":
    weights = read_input(sys.argv[1])
    entanglement = find_best_group1_arrangement(weights, 3)
    print(entanglement)

    entanglement = find_best_group1_arrangement(weights, 4)
    print(entanglement)
