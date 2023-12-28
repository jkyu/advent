import sys
from collections import Counter

def read_input(input):
    with open(input, "r") as f:
        text = f.read().strip()
    return text

def find_floor(text):
    """
    The floor number is the difference between open parentheses
    and close parentheses. Count and return the difference.
    """
    counter = Counter(text)
    return counter["("] - counter[")"]

def find_basement(text):
    """
    Finds the index at which Santa is at the -1 floor for the
    first time. He starts on floor 0. The first instruction has
    index 0, so we add one to this index prior to returning.
    """
    floor = 0
    for i, instruction in enumerate(text):
        if instruction == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            return i+1

if __name__ == "__main__":
    text = read_input(sys.argv[1])
    floor = find_floor(text)
    print(floor)

    basement = find_basement(text)
    print(basement)