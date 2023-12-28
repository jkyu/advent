import sys

def read_grid(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    return lines

def find_empty_rows(grid):
    """Find rows that do not have galaxies."""
    empty_rows = []
    for row in range(len(grid)):
        if "#" not in grid[row]:
            empty_rows.append(row)
    return empty_rows

def find_empty_columns(grid):
    """Find columns that do not have galaxies."""
    cols_without_galaxies = []
    for col in range(len(grid[0])):
        num_galaxies = 0
        for row in range(len(grid)):
            if grid[row][col] == "#":
                num_galaxies += 1
                break
        if num_galaxies == 0:
            cols_without_galaxies.append(col)
    return cols_without_galaxies

def find_galaxy_coords(grid):
    """Get the coordinates of the galaxies in the unexpanded grid."""
    coords = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "#":
                coords.append((row, col))
    return coords

def compute_sum_lengths(grid, empty_rows, empty_cols, expansion_factor):
    """
    Compute the pairwise minimum distances between galaxies.
    Since Up, Down, Left, Right are the only directions that count toward
    the distance, the minimum distance can be computed as the sum of the
    differences in the x and y coordinates of two galaxies.
    To account for potential space expansion, check if there are empty rows
    or columns between two galaxies. For empty row or column between two
    galaxies, add a distance equivalent to expansion_factor-1. 
    One is subtracted from the expansion factor to avoid double counting
    of the original unexpanded row/column.
    """
    galaxy_coords = find_galaxy_coords(grid)
    sum_lengths = 0
    for i in range(len(galaxy_coords)):
        for j in range(i+1, len(galaxy_coords)):
            galaxy1 = galaxy_coords[i]
            galaxy2 = galaxy_coords[j]
            distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])
            for empty_row in empty_rows:
                if galaxy1[0] < empty_row < galaxy2[0] or galaxy2[0] < empty_row < galaxy1[0]:
                    distance += expansion_factor-1
            for empty_col in empty_cols:
                if galaxy1[1] < empty_col < galaxy2[1] or galaxy2[1] < empty_col < galaxy1[1]:
                    distance += expansion_factor-1
            sum_lengths += distance
    return sum_lengths

if __name__ == "__main__":
    grid = read_grid(sys.argv[1])
    empty_rows = find_empty_rows(grid)
    empty_cols = find_empty_columns(grid)
    # expansion_factor=2 because every empty/row column is doubled
    sum_lengths = compute_sum_lengths(grid, empty_rows, empty_cols, 2)
    print(sum_lengths)
    
    # part 2: expansion_factor=1000000
    sum_lengths = compute_sum_lengths(grid, empty_rows, empty_cols, 1000000)
    print(sum_lengths)