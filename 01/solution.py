def get_calibration_value_part1(line):
    """part 1"""
    value = 0
    for i in range(len(line)-1, -1, -1):
        if line[i].isnumeric():
            value += int(line[i])
            break
    for i in range(len(line)):
        if line[i].isnumeric():
            value += 10*int(line[i])
            break
    print(value)
    return value

numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
           "eight": 8, "nine": 9}
reversed_numbers = {"".join(reversed(key)): val for key, val in numbers.items()}

class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.number = None
        self.children = {}

    def __repr__(self):
        return str(self.__dict__)

root = TrieNode()
for number_key, number_val in numbers.items():
    level = root
    for char in number_key:
        if char not in level.children:
            level.children[char] = TrieNode(char)
        level = level.children[char]
    level.number = number_val

def get_calibration_value_part2(line):
    numbers = []
    for i in range(len(line)):
        if line[i].isnumeric():
            numbers.append(int(line[i])) 
        elif line[i] in root.children:
            j = i
            level = root
            while j < len(line) and line[j] in level.children:
                level = level.children[line[j]]
                if level.number is not None:
                    numbers.append(level.number)
                j += 1
    return numbers[0]*10 + numbers[-1]

total = 0
with open("input.txt", "r") as input:
    for line in input:
        total += get_calibration_value_part2(line)
print(total)
