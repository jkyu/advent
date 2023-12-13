import sys

def read_input(input):
    with open(input, "r") as f:
        blocks = f.read().strip().split("\n\n")
    blocks = [block.splitlines() for block in blocks]
    return blocks

def transpose_block(block):
    blockT = []
    for col in range(len(block[0])):
        lineT = []
        for row in range(len(block)):
            lineT.append(block[row][col])
        blockT.append("".join(lineT))
    return blockT

def transpose_blocks(blocks):
    return [transpose_block(block) for block in blocks]

def find_num_differences(row1, row2):
    num_diffs = sum(1 for i, j in zip(row1, row2) if i != j)
    return num_diffs

def find_mirror_with_smudge(block):
    """
    Finds a horizontal mirror by allowing for one smudge.
    The smudge can be found if a palindrome check fails only because of a
    single difference between two rows (caused by the smudge).
    If more than one smudge needs to be present, the mirror placement was not valid.
    The mirror placement now requires exactly one smudge, so previous
    mirror placements without the smudge are no longer valid.
    """
    for row in range(len(block)-1):
        length = min(row+1, len(block)-1-row)
        found_mirror = True
        num_smudges = 0
        for i in range(length):
            if block[row-i] != block[row+1+i]:
                num_differences = find_num_differences(block[row-i], block[row+1+i])
                if num_differences != 1: # more than one diff. not smudge
                    found_mirror = False
                    break
                else:
                    num_smudges += 1
        if found_mirror and num_smudges == 1:
            return row+1
    return 0

def find_mirror(block):
    """
    Find the horizontal mirror. The rows form a palindrome around the mirror.
    Try placing a mirror behind each row and check that the placement is
    valid by comparing rows outward from the mirror. 
    A length for how far to go on one side of the mirror is computed by 
    taking the minimum of the distance from the row to the top or to the
    bottom, since anything outside of that range cannot be reflected.
    A mirror placement is valid if reflected rows are equivalent for the
    entire length. 
    Assuming only one mirror can be placed for each pattern, quit immediately
    once a valid mirror placement is found.
    """
    for row in range(len(block)-1):
        length = min(row+1, len(block)-1-row)
        found_mirror = True
        for i in range(length):
            if block[row-i] != block[row+1+i]:
                found_mirror = False
                break
        if found_mirror:
            return row+1
    return 0

def sum_rows_above_mirrors(blocks, has_smudge):
    """sum number of rows above the mirror for all blocks"""
    if has_smudge:
        return sum(find_mirror_with_smudge(block) for block in blocks)
    else:
        return sum(find_mirror(block) for block in blocks)

def sum_rows_and_cols_before_mirrors(blocks, blocksT, has_smudge=False):
    sum_cols = sum_rows_above_mirrors(blocksT, has_smudge)
    sum_rows = 100 * sum_rows_above_mirrors(blocks, has_smudge)
    return sum_rows + sum_cols

if __name__ == "__main__":
    blocks = read_input(sys.argv[1]) # get row mirrors
    # easier to just transpose the pattern to find vertical mirrors
    blocksT = transpose_blocks(blocks) # get column mirrors
    p1 = sum_rows_and_cols_before_mirrors(blocks, blocksT)
    print(p1)

    p2 = sum_rows_and_cols_before_mirrors(blocks, blocksT, has_smudge=True)
    print(p2)
