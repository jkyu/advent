import sys

from dataclasses import dataclass
from queue import Queue
from typing import Set

@dataclass
class Brick:
    label: int
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int
    supported_bricks: Set[int]
    supported_by: Set[int]

    def update_z(self, new_zmin):
        height = self.zmax - self.zmin
        self.zmin = new_zmin
        self.zmax = new_zmin + height
    
    def has_collision(self, other):
        """
        Assuming z-coordinates overlap, only one of the x or y
        coordinates at most can over overlaps with the other brick.

        Overlaps can occur in the following ways (other cases not
        listed are covered by checking for these).
        Case 1:
           [xmin   xmax]
        [xmin'    xmax']

        Case 2:
           [xmin   xmax]
              [xmin'    xmax']

        Case 3:
           [xmin   xmax]
        [xmin'       xmax']

        If such overlaps occur in both the x and y coordinates, then
        there is a collision in the xy plane.
        """
        n_overlaps = 0
        # overlap in x
        if self.xmin <= other.xmin <= self.xmax or self.xmin <= other.xmax <= self.xmax or other.xmin <= self.xmin <= other.xmax:
            n_overlaps += 1
        # overlap in y
        if self.ymin <= other.ymin <= self.ymax or self.ymin <= other.ymax <= self.ymax or other.ymin <= self.ymin <= other.ymax:
            n_overlaps += 1
        return n_overlaps == 2

def read_input(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    bricks = []
    for i, line in enumerate(lines):
        left, right = line.split("~")
        left = [int(num) for num in left.split(",")]
        right = [int(num) for num in right.split(",")]
        xmin = min(left[0], right[0])
        xmax = max(left[0], right[0])
        ymin = min(left[1], right[1])
        ymax = max(left[1], right[1])
        zmin = min(left[2], right[2])
        zmax = max(left[2], right[2])
        brick = Brick(i, xmin, xmax, ymin, ymax, zmin, zmax, set(), set())
        bricks.append(brick)
    return bricks

def drop_bricks(bricks):
    """
    Drop bricks into the correct locations. The algorithm is as follows:
    1. Sort the bricks to start with the bricks that have the lowest zmin first.
       Bricks drop at the same rate, so the lower bricks determine the structure
       of the stack.
    2. For each brick:
        - search for bricks at known heights z. These known heights are
        sorted so that the highest height appears first in the search. Check if
        the current falling brick collides with any brick that is at rest at level
        z.
        - if no collision is found, move to the next z-level known to contain the
        top of a block until a collision is found (possibly with the ground)
        - once a collision is found, the brick is to be placed at the z-level + 1.
        The lower end of the z-coordinate should be placed here.
    3. Store the high end of the z-coordinate because any block that is supported
       by this current block must rest on top of it. If no other block has been 
       observed at this z-level, we must add the z-level to our list of known
       heights and re-sort. 
    """
    bricks.sort(key = lambda x: x.zmin)
    # special brick to represent the ground at z=0
    ground = Brick(
        label=None,
        xmin=-sys.maxsize,
        xmax=sys.maxsize,
        ymin=-sys.maxsize,
        ymax=sys.maxsize,
        zmin=-sys.maxsize,
        zmax=sys.maxsize,
        supported_bricks=set(),
        supported_by=set(),
    )
    level_to_bricks = {0: [ground]}
    levels = [0]
    for brick in bricks:
        found_supporting_brick = False
        for level in levels:
            for placed_brick in level_to_bricks[level]:
                if placed_brick.has_collision(brick):
                    found_supporting_brick = True
                    placed_brick.supported_bricks.add(brick.label)
                    brick.supported_by.add(placed_brick.label)
            if found_supporting_brick:
                break
        height = level + 1
        brick.update_z(height)
        if brick.zmax not in level_to_bricks:
            level_to_bricks[brick.zmax] = []
            levels.append(brick.zmax)
            levels.sort(reverse=True)
        level_to_bricks[brick.zmax].append(brick)

def find_bricks_to_disintegrate(labeled_bricks):
    """
    for each brick, check the bricks it supports. if any of the
    supported bricks is supported by only one brick, then that
    one brick must be the current brick, which is deemed to be
    structural and therefore not a candidate for disintegration.
    """
    can_disintegrate = set()
    for brick in labeled_bricks.values():
        if len(brick.supported_bricks) == 0:
            can_disintegrate.add(brick.label)
        else:
            is_structural_support = False
            for label in brick.supported_bricks:
                if len(labeled_bricks[label].supported_by) == 1:
                    is_structural_support = True
                    break
            if not is_structural_support:
                can_disintegrate.add(brick.label)
    return can_disintegrate

def count_chain_reaction(start, labeled_bricks):
    """
    Disintegrate the brick labeled start. Any bricks that are
    supported only by bricks that have already fallen (or the
    initial disintegrated brick) will also fall.
    """
    queue = Queue()
    queue.put(start)
    fallen_bricks = set()
    fallen_bricks.add(start)
    while not queue.empty():
        brick = labeled_bricks[queue.get()]
        for label in brick.supported_bricks:
            supported_brick = labeled_bricks[label]
            # check that the supporting bricks are a subset
            # of the already fallen/disintegrated
            if supported_brick.supported_by <= fallen_bricks:
                if label not in fallen_bricks:
                    fallen_bricks.add(label)
                    queue.put(label)
    # subtract one because the initial brick is disintegrated
    # and not one of the fallen bricks
    return len(fallen_bricks) - 1

def sum_chain_reactions(labeled_bricks, structural_brick_labels):

    total = 0
    for label in structural_brick_labels:
        total += count_chain_reaction(label, labeled_bricks)
    return total

if __name__ == "__main__":
    bricks = read_input(sys.argv[1])
    drop_bricks(bricks)
    labeled_bricks = {brick.label: brick for brick in bricks}
    can_disintegrate = find_bricks_to_disintegrate(labeled_bricks)
    print(len(can_disintegrate))

    labels = set(labeled_bricks.keys())
    structural_brick_labels = labels.difference(can_disintegrate)
    sum_fallen = sum_chain_reactions(labeled_bricks, structural_brick_labels)
    print(sum_fallen)