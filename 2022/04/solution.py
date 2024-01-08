import re
import sys

from dataclasses import dataclass
from typing import List


@dataclass
class Range:
    low: int
    high: int

    def contains(self, other):
        """
        self:  [low       high]
        other:    [low   high]
        """
        return self.low <= other.low and self.high >= other.high

    def overlaps_with(self, other):
        """
        Cases:
        self:  [low    high]
        other:     [low      high]

        self:      [low      high]
        other: [low    high]
        """
        return self.low <= other.low <= self.high or other.low <= self.low <= other.high


@dataclass
class Pair:
    elf1: Range
    elf2: Range

    @property
    def has_complete_overlap(self):
        return self.elf1.contains(self.elf2) \
            or self.elf2.contains(self.elf1)

    @property
    def has_overlap(self):
        return self.elf1.overlaps_with(self.elf2)


def read_input(file_name: str) -> List[Pair]:
    with open(file_name, "r") as f:
        lines = f.read().strip().splitlines()
    pairs = []
    for line in lines:
        numbers = re.findall(r'\b[0-9]+\b', line)
        range1 = Range(int(numbers[0]), int(numbers[1]))
        range2 = Range(int(numbers[2]), int(numbers[3]))
        pair = Pair(range1, range2)
        pairs.append(pair)
    return pairs


def number_of_pairs_with_complete_overlap(pairs: List[Pair]) -> int:
    return sum(pair.has_complete_overlap for pair in pairs)


def number_of_pairs_with_any_overlap(pairs: List[Pair]) -> int:
    return sum(pair.has_overlap for pair in pairs)


if __name__ == "__main__":
    elf_pairs = read_input(sys.argv[1])
    count = number_of_pairs_with_complete_overlap(elf_pairs)
    print("Part 1:", count)

    count = number_of_pairs_with_any_overlap(elf_pairs)
    print("Part 2:", count)
