import sys

DIRECTIONS = {
    ">": 1,
    "<": -1,
    "^": 1j,
    "v": -1j,
}

def read_input(input):
    with open(input, "r") as f:
        text = f.read().strip()
    return text

def count_houses_that_get_presents(directions, start=(0+0j), with_robo=False):
    addresses = set()
    addresses.add(start)
    santa_location = start
    robo_location = start
    for i, direction in enumerate(directions):
        if with_robo:
            if i % 2 == 0:
                santa_location += DIRECTIONS[direction]
                addresses.add(santa_location)
            else:
                robo_location += DIRECTIONS[direction]
                addresses.add(robo_location)
        else:
            santa_location += DIRECTIONS[direction]
            addresses.add(santa_location)
    return len(addresses)

if __name__ == "__main__":
    directions = read_input(sys.argv[1])
    houses = count_houses_that_get_presents(directions)
    print(houses)

    houses = count_houses_that_get_presents(directions, with_robo=True)
    print(houses)
