import sys
from dataclasses import dataclass

@dataclass
class Mapping:
    destination: int
    source: int
    length: int

@dataclass
class Seed:
    start: int
    end: int

def read_maps(input):
    with open(input) as f:
        text = f.read().strip()
        lines = text.split("\n")
        blocks = text.split("\n\n")
    seed_block, *map_blocks = blocks
    seeds = [int(x) for x in seed_block.split(":")[1].split()]
    layers = []
    for block in map_blocks:
        lines = block.split("\n")[1:]
        maps = []
        for line in lines:
            destination, source, length = line.split()
            maps.append(Mapping(int(destination), int(source), int(length)))
        layers.append(maps)
    return seeds, layers

def map_source_to_destination(source, layer):
    """
    If the source is in any of the mapping ranges,
    then return the destination as computed
    by the mapping. Otherwise, source == destination.
    """
    for mapping in layer:
        if mapping.source <= source <= mapping.source + mapping.length:
            return source + mapping.destination - mapping.source
    return source

def map_ranges_to_destination_ranges(ranges, layer):
    """
    Take in a set of ranges and find intersections
    with the next layer of mappings.
    Example: in layer 1, there is only one range, [seed_start, seed_end)
    [seed_start                  seed_end)
           [source   source+length]
    [lower][intersection          ][upper)

    We want to keep [lower] and [upper) because those
    might be ranges where source == destination.
    We will continue to find intersections with subsequent
    input ranges, but any leftover [lower] and [upper)
    ranges at the end are ranges where source == destination.
    """
    destination_ranges = []
    for mapping in layer:
        source_end = mapping.source + mapping.length
        leftover_ranges = []
        while len(ranges) > 0:
            start, end = ranges.pop()
            lower = (start, min(end, mapping.source))
            upper = (max(start, source_end), end)
            intersection = (max(start, mapping.source), min(end, source_end))
            if lower[1] > lower[0]: # nonempty:
                leftover_ranges.append(lower)
            if intersection[1] > intersection[0]:
                destination_start = intersection[0] - mapping.source + mapping.destination
                destination_end = intersection[1] - mapping.source + mapping.destination
                destination_ranges.append((destination_start, destination_end))
            if upper[1] > upper[0]:
                leftover_ranges.append(upper)
        ranges = leftover_ranges
    return destination_ranges + ranges

if __name__=="__main__":
    seeds, layers = read_maps(sys.argv[1])
    minimum_location = sys.maxsize
    for seed in seeds:
        curr = seed
        for layer in layers:
            curr = map_source_to_destination(curr, layer)
        minimum_location = min(minimum_location, curr)
    print(minimum_location)

    seed_ranges = []
    minimum_location2 = sys.maxsize
    for i in range(len(seeds)//2):
        seed_start = seeds[2*i]
        seed_end = seed_start + seeds[2*i+1]
        seed_ranges.append((seed_start, seed_end))
    for seed_range in seed_ranges:
        curr_ranges = [seed_range]
        for layer in layers:
            curr_ranges = map_ranges_to_destination_ranges(curr_ranges, layer)
        minimum_location2 = min(minimum_location2, min(curr_ranges)[0])
    print(minimum_location2)
        