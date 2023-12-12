import sys

from functools import lru_cache

def read_input(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    grid = []
    arrangements = []
    for line in lines:
        row, arrangement = line.split()
        grid.append(row)
        arrangement = tuple(int(x) for x in arrangement.split(","))
        arrangements.append(arrangement)
    return grid, arrangements

@lru_cache # memoize recursive solution
def find_valid_arrangements(springs, blocks):
    # base case: finished the row
    if len(springs) == 0:
        # also completed placing the blocks, so valid
        if len(blocks) == 0:
            return 1
        # could not place all blocks, so not valid
        else:
            return 0

    # case 1: current row index is a working spring. go to next index.
    if springs[0] == ".":
        return find_valid_arrangements(springs[1:], blocks)

    # case 2: current row index is unknown. two branches:
    # 2a: the unknown is a working spring
    # 2b: the unknown is a broken spring
    if springs[0] == "?":
        working_case = find_valid_arrangements(springs[1:], blocks)
        broken_case = find_valid_arrangements(springs.replace("?", "#", 1), blocks)
        return working_case + broken_case
    
    # case 3: current row index is broken
    if springs[0] == "#":
        # 3a. have broken spring but unable to place into valid arrangement
        if len(blocks) == 0:
            return 0
        # 3b. have fewer springs left than specified by arrangement. not valid
        if len(springs) < blocks[0]:
            return 0
        # 3c. have working spring before the continuous number of broken springs is satisfied. not valid.
        if "." in springs[:blocks[0]]:
            return 0
        # 3d. can make a valid arrangement
        # but need to check following spring if expecting additional blocks of broken springs
        if len(blocks) > 1:
            # have no space for another block after this one. cannot be valid
            if len(springs) < blocks[0] + 1:
                return 0
            # spring following this block is also broken. not valid.
            if springs[blocks[0]] == "#":
                return 0
            springs = springs[blocks[0]+1:]
        # 3e. can make valid arrangement and this is the last block to satisfy.
        # if the following spring is broken, 3b will catch it.
        else:
            springs = springs[blocks[0]:]
        return find_valid_arrangements(springs, blocks[1:])

if __name__ == "__main__":
    grid, blocks = read_input(sys.argv[1])
    part1 = 0
    for springs, block in zip(grid, blocks):
        part1 += find_valid_arrangements(springs, block)
    print(part1)

    part2 = 0
    for springs, block in zip(grid, blocks):
        springs = "?".join([springs]*5)
        block = block*5
        part2 += find_valid_arrangements(springs, block)
    print(part2)
