import sys

from dataclasses import dataclass
from typing import List

@dataclass
class Reindeer:
    name: str
    speed: int
    fly_duration: int
    rest_duration: int

    @property
    def cycle_length(self):
        return self.fly_duration + self.rest_duration

    def distance_traveled(self, time: int) -> int:
        n_cycles = time // self.cycle_length
        leftover_time = time % self.cycle_length
        # distance for each full cycle is the same
        distance = n_cycles * self.speed * self.fly_duration
        # for the incomplete cycle, the reindeer might be 
        # in the middle of flying or already done flying
        distance += min(leftover_time, self.fly_duration) * self.speed
        return distance

    def __hash__(self):
        return hash(self.name)

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    reindeer = []
    for line in lines:
        line = line.split()
        name = line[0]
        speed = int(line[3])
        fly_duration = int(line[6])
        rest_duration = int(line[-2])
        reindeer.append(
            Reindeer(name, speed, fly_duration, rest_duration)
        )
    return reindeer

def find_farthest_after_time_cutoff(
        reindeer: List[Reindeer],
        time: int,
    ) -> int:
    winning_distance = -sys.maxsize
    for deer in reindeer:
        distance = deer.distance_traveled(time)
        winning_distance = max(winning_distance, distance)
    return winning_distance

def find_highest_score(
        reindeer: List[Reindeer],
        time: int,
    ) -> int:
    scores = {deer: 0 for deer in reindeer}
    for i in range(1, time+1):
        current_leaders = []
        leading_distance = -sys.maxsize
        for deer in reindeer:
            distance = deer.distance_traveled(i)
            # deer is leading by itself
            if distance > leading_distance:
                current_leaders = [deer]
                leading_distance = distance
            # deer is tied in the provisional lead
            elif distance == leading_distance:
                current_leaders.append(deer)
        # give point to leader(s) at this time point
        for leader in current_leaders:
            scores[leader] += 1
    return max(scores.values())

if __name__ == "__main__":
    reindeer = read_input(sys.argv[1])
    distance = find_farthest_after_time_cutoff(reindeer, 2503)
    print(distance)

    distance = find_highest_score(reindeer, 2503)
    print(distance)
