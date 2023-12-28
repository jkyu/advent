from collections import deque
# what are the symbols we care about?

SYMBOLS = set()
with open("input.txt", "r") as input:
    for line in input:
        for char in line.strip():
            if not char.isalnum():
                SYMBOLS.add(char)
SYMBOLS.discard(".")
SEARCH_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]

# turn the input into a graph (matrix)
def convert_input_to_graph(input_file):
    grid = []
    with open(input_file, "r") as input:
        for line in input:
            grid.append(list(line.strip()))
    return grid

# look for special symbols
def find_part_num_sum(grid):
    part_num_sum = 0
    # do not allow searched parts to be duplicated
    visited = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] in SYMBOLS:
                part_num_sum += sum(find_connected_parts(grid, row, col, visited))
    return part_num_sum

def find_gear_ratio_sum(grid):
    gear_ratio_sum = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "*":
                # unlike the previous task, one part may be connected to multiple gears
                # deduplicate per gear, not overall
                visited = set()
                connected_parts = find_connected_parts(grid, row, col, visited)
                if len(connected_parts) == 2:
                    gear_ratio_sum += connected_parts[0] * connected_parts[1]
    return gear_ratio_sum
            
def find_connected_parts(grid, row, col, visited):
    parts = []
    for dx, dy in SEARCH_DIRECTIONS:
        new_row = row+dx
        new_col = col+dy
        if (new_row, new_col) in visited:
            continue
        if new_row >= 0 and new_row < len(grid) and new_col >= 0 and new_col < len(grid[0]):
            if grid[new_row][new_col].isnumeric():
                parts.append(find_part_number(grid, new_row, new_col, visited))
    return parts

def find_part_number(grid, row, col, visited):
    digits = deque()
    digits.append(int(grid[row][col]))
    visited.add((row, col))
    left_cursor = col - 1
    while left_cursor >= 0 and grid[row][left_cursor].isnumeric():
        digits.appendleft(int(grid[row][left_cursor]))
        visited.add((row, left_cursor))
        left_cursor -= 1
    right_cursor = col + 1
    while right_cursor < len(grid[0]) and grid[row][right_cursor].isnumeric():
        digits.append(int(grid[row][right_cursor]))
        visited.add((row, right_cursor))
        right_cursor += 1
    part = 0
    while len(digits) > 0:
        part = part*10 + digits.popleft()
    return part

if __name__=="__main__":
    grid = convert_input_to_graph("input.txt")
    solution = find_part_num_sum(grid)
    print(solution)
    solution2 = find_gear_ratio_sum(grid)
    print(solution2)



