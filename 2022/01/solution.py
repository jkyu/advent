import sys

from queue import PriorityQueue
from typing import List


def read_input(file):
    with open(file, "r") as f:
        blocks = f.read().strip().split("\n\n")
    elf_inventories = []
    for block in blocks:
        lines = block.splitlines()
        elf_inventories.append([int(x) for x in lines])
    return elf_inventories


def find_highest_calorie_inventories(
        inventories: List[int],
        limit: int = 1,
) -> List[int]:
    """
    Use a min heap to store up to limit number
    of calorie inventories. This only keeps the
    largest limit inventories since the smallest
    values always end up at the top of the heap.
    """
    heap = PriorityQueue()
    for inventory in inventories:
        heap.put(sum(inventory))
        if heap.qsize() > limit:
            heap.get()
    kept_inventories = []
    while not heap.empty():
        kept_inventories.append(heap.get())
    return kept_inventories


if __name__ == "__main__":
    inventories = read_input(sys.argv[1])
    largest_inventories = find_highest_calorie_inventories(inventories, 1)
    print(sum(largest_inventories))

    largest_inventories = find_highest_calorie_inventories(inventories, 3)
    print(sum(largest_inventories))
