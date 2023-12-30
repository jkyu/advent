import re
import sys

from dataclasses import dataclass
from typing import List

@dataclass
class Sue:
    number: int = None
    goldfish: int = None
    samoyeds: int = None
    akitas: int = None
    vizslas: int = None
    pomeranians: int = None
    perfumes: int = None
    cats: int = None
    trees: int = None
    children: int = None
    cars: int = None

def read_input(file: str) -> List[Sue]:
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    sues = []
    for line in lines:
        chunks = re.findall(r'\b\w+\b', line)
        cleaned = [
            re.sub(r'[^a-zA-Z0-9]', '', chunk) for chunk in chunks
        ]
        sue = Sue(number=int(cleaned[1]))
        setattr(sue, cleaned[2], int(cleaned[3]))
        setattr(sue, cleaned[4], int(cleaned[5]))
        setattr(sue, cleaned[6], int(cleaned[7]))
        sues.append(sue)
    return sues

def find_sue(
        sues: List[Sue],
        ref_sue: Sue,
        things: List[str],
        outdated=False
    ) -> int:
    """
    Find the Sue in question by iteratively eliminating
    Sues that cannot be the reference Sue who sent the gift.

    If the retroencabulator is outdated, the elimination process
    relaxes the filter on cats and trees so that all values
    greater than the reference are kept and on pomeranians
    and goldfish so that all values less than the reference
    are kept. In all other cases, an exact match between
    the reference and sue value is required.
    """
    possible_sues = set([sue.number for sue in sues])
    for thing in things:
        for sue in sues:
            # ignore sues already eliminated
            if not sue.number in possible_sues:
                continue
            target = getattr(ref_sue, thing)
            val = getattr(sue, thing)
            # do not eliminate sue if the number of
            # this thing she owns is unknown
            if val is None:
                continue
            if outdated and thing in {"cats", "trees"}:
                if not val > target:
                    possible_sues.remove(sue.number)
            elif outdated and thing in {"pomeranians", "goldfish"}:
                if not val < target:
                    possible_sues.remove(sue.number)
            else:
                if target != val:
                    possible_sues.remove(sue.number)
    if len(possible_sues) != 1:
        raise Exception(
            "There should only be one Sue left after filtering."
        )
    return possible_sues.pop()

if __name__ == "__main__":
    sues = read_input(sys.argv[1])

    things = [
        "children",
        "cats",
        "samoyeds",
        "pomeranians",
        "akitas",
        "vizslas",
        "goldfish",
        "trees",
        "cars",
        "perfumes",
    ]

    ref_sue = Sue(
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )

    sue_number = find_sue(sues, ref_sue, things)
    print(sue_number)

    sue_number = find_sue(sues, ref_sue, things, True)
    print(sue_number)
