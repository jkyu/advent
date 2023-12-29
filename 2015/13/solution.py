import sys

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    happiness = {}
    for line in lines:
        line = [x.strip() for x in line.split()]
        person = line[0]
        neighbor = line[-1][:-1] # remove the period
        if line[2] == "gain":
            sign = 1
        else:
            sign = -1
        happiness_units = sign * int(line[3])
        if person not in happiness:
            happiness[person] = {}
        happiness[person][neighbor] = happiness_units
    return happiness

def place_person(pairs, seated, arrangement):
    """
    Seat people clockwise and count the happiness they
    get being placed next to the person on their right.
    Also count the happiness the person on the right
    gets from having this new person on their left.

    When all people are seated, the first person finally
    gets to add happiness for the person now on their right.
    """
    # all people seated. need to count the happiness from the
    # first and last person being seated next to each other
    if len(seated) == len(pairs):
        first_seated = arrangement[0]
        last_seated = arrangement[-1]
        happiness = pairs[last_seated][first_seated]
        happiness += pairs[first_seated][last_seated]
        return happiness

    # try all seating arrangements and pick the one 
    # that results in most happiness
    happiness_subtotal = -sys.maxsize
    for person in pairs.keys():
        # person is already seated. ignore.
        if person in seated:
            continue

        # happiness resulting from placing current person
        # next to previously seated person, taking into
        # account the perspective of both people
        happiness = pairs[person][arrangement[-1]]
        happiness += pairs[arrangement[-1]][person]

        # seat the person and continue placements with
        # remaining people. keep the arragement that
        # generates maximum happiness
        seated.add(person)
        arrangement.append(person)
        happiness += place_person(pairs, seated, arrangement)
        happiness_subtotal = max(happiness_subtotal, happiness)
        seated.remove(person)
        arrangement.pop()

    return happiness_subtotal

def find_optimal_arrangement(pairs):
    keys = set(happiness_pairs.keys())
    first = keys.pop()
    arrangement = [first]
    seated = set(arrangement)
    return place_person(pairs, seated, arrangement)

if __name__ == "__main__":
    happiness_pairs = read_input(sys.argv[1])
    happiness = find_optimal_arrangement(happiness_pairs)
    print(happiness)

    # add self to happiness graph
    me = "Me"
    happiness_pairs[me] = {}
    for name in happiness_pairs:
        happiness_pairs[name][me] = 0
        happiness_pairs[me][name] = 0
    happiness = find_optimal_arrangement(happiness_pairs)
    print(happiness)
