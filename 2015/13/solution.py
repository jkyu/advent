import sys

from dataclasses import dataclass
from typing import List, Dict


def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    happiness = {}
    for line in lines:
        line = [x.strip() for x in line.split()]
        person = line[0]
        neighbor = line[-1][:-1]  # remove the period
        if line[2] == "gain":
            sign = 1
        else:
            sign = -1
        happiness_units = sign * int(line[3])
        if person not in happiness:
            happiness[person] = {}
        happiness[person][neighbor] = happiness_units
    return happiness


@dataclass
class State:
    last_seated: str
    currently_seated: str

    def __hash__(self):
        return hash((self.last_seated, self.currently_seated))


def assign_seat(
        names: List[str],
        pairs: Dict[str, Dict[str, int]],
        seated: List[int],
        last_seated: str,
        cache: Dict[State, int],
) -> int:
    # base case: everyone is seated. return the happiness
    # resulting from seating the final person next to the first
    if all(seated):
        happiness = pairs[last_seated][names[0]]
        happiness += pairs[names[0]][last_seated]
        return happiness

    # the state contains the previous person seated and a bit
    # string that denotes who has been or remains to be seated
    state = State(last_seated, "".join(list(map(str, seated))))
    if state in cache:
        return cache[state]

    max_happiness = -sys.maxsize
    for i in range(len(names)):
        person = names[i]
        if seated[i] == 1:
            continue
        # seat the person
        seated[i] = 1
        # happiness from seating this person next to the
        # previously seated person
        happiness = pairs[person][last_seated] + pairs[last_seated][person]
        # optimal seating arrangement for the remainder of people
        happiness += assign_seat(names, pairs, seated, person, cache)
        max_happiness = max(max_happiness, happiness)
        # unseat the person to try another arrangement
        seated[i] = 0

    cache[state] = max_happiness
    return max_happiness


def find_optimal_arrangement(pairs):
    keys = list(happiness_pairs.keys())
    seated = [0 for _ in range(len(keys))]
    # because the table is round, the first
    # to be seated does not matter
    seated[0] = 1
    cache = {}
    max_happiness = assign_seat(keys, pairs, seated, keys[0], cache)
    return max_happiness


if __name__ == "__main__":
    happiness_pairs = read_input(sys.argv[1])
    optimal_happiness = find_optimal_arrangement(happiness_pairs)
    print(optimal_happiness)

    # add self to happiness graph
    me = "Me"
    happiness_pairs[me] = {}
    for name in happiness_pairs:
        happiness_pairs[name][me] = 0
        happiness_pairs[me][name] = 0
    optimal_happiness = find_optimal_arrangement(happiness_pairs)
    print(optimal_happiness)
