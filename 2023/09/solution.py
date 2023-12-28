import sys
from typing import List

def read_input(input: str):
    with open(input, "r") as f:
        text = f.read().strip()
        lines = text.split("\n")
    lines = [[int(x) for x in line.split()] for line in lines]
    return lines

def extrapolate(nums: List[int], add: bool):
    if all([x==0 for x in nums]):
        return 0
    differences = []
    for i in range(1, len(nums)):
        differences.append(nums[i] - nums[i-1])
    increment = extrapolate(differences, add)
    if add:
        extrapolated_value = nums[-1] + increment
    else:
        extrapolated_value = nums[0] - increment
    return extrapolated_value

def find_sum_history(num_lines: List[List[int]], add=True):
    sum_history = 0
    for nums in num_lines:
        val = extrapolate(nums, add)
        sum_history += val
    return sum_history

if __name__ == "__main__":
    num_lines = read_input(sys.argv[1])
    sum_history1 = find_sum_history(num_lines, True)
    print(sum_history1)

    sum_history2 = find_sum_history(num_lines, False)
    print(sum_history2)
