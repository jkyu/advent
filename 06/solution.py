import math
import sys

from dataclasses import dataclass

@dataclass
class Race:
    time: int
    distance: int

    def parabola(self, x):
        return x * self.time - x*x - self.distance

    @property
    def parabola_argmax(self):
        return self.time // 2

def read_races(input):
    with open(input) as f:
        text = f.read().strip()
        lines = text.split("\n")
    times_txt, distances_txt = [line.split(":")[1] for line in lines]
    times = [int(time) for time in times_txt.split()]
    distances = [int(distance) for distance in distances_txt.split()]
    races = [Race(time, distance) for (time, distance) in zip(times, distances)]
    return races

def count_ways_to_win(races):
    """
    Do binary search to find sign changes by the parabola.
    First, we find the argmax x=c using the derivative of the
    parabola, and then we search in the intervals [0, c] and
    [c, time] to find the sign change points.
    x=a is the smallest x for which the parabola is positive.
    x=b is the largest x for which the parabola is positive.
    Number of ways to win a race is the number of integers
    in the interval [a, b]
    """
    ways_to_win = []
    for race in races:
        a = find_smallest_positive(race)
        b = find_largest_positive(race)
        ways = b - a + 1 
        # ways = 0
        # for x in range(race.time):
        #     if race.parabola(x) > 0:
        #         ways += 1
        ways_to_win.append(ways)
    return math.prod(ways_to_win)

def find_smallest_positive(race):
    low = 0
    high = race.parabola_argmax
    a = high
    while low <= high and race.parabola(high) > 0:
        mid = (low+high) // 2
        val = race.parabola(mid)
        if val > 0:
            high = mid - 1
            a = mid
        else:
            low = mid + 1
    return a

def find_largest_positive(race):
    low = race.parabola_argmax
    high = race.time
    b = low
    while low <= high and race.parabola(low) > 0:
        mid = (low+high) // 2
        val = race.parabola(mid)
        if val > 0:
            low = mid + 1
            b = mid
        else:
            high = mid - 1
    return b

def remove_kerning_from_races(races):
    times = [str(race.time) for race in races]
    distances = [str(race.distance) for race in races]

    time = int("".join(times))
    distance = int("".join(distances))
    return Race(time, distance)

if __name__ == "__main__":
    races = read_races(sys.argv[1])
    # part 1
    ways_to_win1 = count_ways_to_win(races)
    print(ways_to_win1)

    # part 2: there's actually only one race
    race = remove_kerning_from_races(races)
    ways_to_win2 = count_ways_to_win([race])
    print(ways_to_win2)
