import sys

from dataclasses import dataclass
from typing import List

PRIORITY_VALUES = {}
base_a = ord("a")
base_A = ord("A")
for i in range(26):
    PRIORITY_VALUES[chr(base_a + i)] = i + 1
    PRIORITY_VALUES[chr(base_A + i)] = i + 27


@dataclass
class Rucksack:
    contents: str

    @property
    def content_set(self):
        return set(self.contents)

    @property
    def compartment1(self):
        return set(self.contents[:len(self.contents) // 2])

    @property
    def compartment2(self):
        return set(self.contents[len(self.contents) // 2:])

    def find_shared_item(self):
        shared_items = self.compartment1.intersection(self.compartment2)
        if len(shared_items) != 1:
            raise ValueError(
                "There should be exactly one shared "
                + "item type between compartments."
            )
        return shared_items.pop()


def read_input(file_name: str) -> List[Rucksack]:
    with open(file_name, "r") as f:
        lines = f.read().strip().splitlines()
    return [Rucksack(line.strip()) for line in lines]


def priority_sum_of_redundant_items(rucksacks: List[Rucksack]):
    """
    Perform set intersections between compartments to find
    the redundant item type between the two compartments.
    """
    priority_sum = 0
    for sack in rucksacks:
        shared_item = sack.find_shared_item()
        priority_sum += PRIORITY_VALUES[shared_item]
    return priority_sum


def priority_sum_of_badges(rucksacks: List[Rucksack]):
    """
    Every three consecutive rucksacks form a group. Each group
    should contain exactly one redundant item, which is the
    badge. This can be found as the intersection of the three
    rucksacks.
    """
    n_groups = len(rucksacks) // 3
    group = 0
    priority_sum = 0
    while group < n_groups:
        sack1 = rucksacks[3 * group].content_set
        sack2 = rucksacks[3 * group + 1].content_set
        sack3 = rucksacks[3 * group + 2].content_set
        badges = sack1.intersection(sack2, sack3)
        if len(badges) != 1:
            raise ValueError(
                "There should be exactly one badge in a group."
            )
        priority_sum += PRIORITY_VALUES[badges.pop()]
        group += 1
    return priority_sum


if __name__ == "__main__":
    sacks = read_input(sys.argv[1])
    total_priority = priority_sum_of_redundant_items(sacks)
    print("Priority sum of shared item types:", total_priority)

    total_priority = priority_sum_of_badges(sacks)
    print("Priority sum of badges:", total_priority)
