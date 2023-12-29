import json
import sys

def parse_input(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def find_number_sum(data, ignore_red=False):
    """
    Treat JSON data like a tree and traverse recursively.
    Four cases at each "node" of the tree:
    - the node represents an object (dict). Make a recursive
      call on each value (in the key, value pair) of the node.
      If objects containing "red" should be ignored, then
      exit immediately if a red value is discovered.
    - the node represents a list. Make a recursive call
      on each value of the list.
    - the node represents an int value. Return this value
      to be added to the total.
    - the node is not an int, an object, or list. It will
      not contribute to the number sum, so return 0.
    """
    if type(data) is dict:
        total = 0
        for val in data.values():
            if ignore_red and val == "red":
                return 0
            total += find_number_sum(val, ignore_red)
        return total
    elif type(data) is list:
        return sum(
            [find_number_sum(val, ignore_red) for val in data]
        )
    elif type(data) is int:
        return data
    else:
        return 0

if __name__ == "__main__":
    data = parse_input(sys.argv[1])
    number_sum = find_number_sum(data)
    print(number_sum)

    no_red_sum = find_number_sum(data, True)
    print(no_red_sum)