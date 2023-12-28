import sys

from dataclasses import dataclass

@dataclass
class Present:
    length: int
    width: int
    height: int

    @property
    def sides(self):
        return [
            self.length * self.width,
            self.width * self.height,
            self.height * self.length,
        ]

    @property
    def surface_area(self):
        return sum(self.sides) * 2
    
    @property
    def wrapping_paper(self):
        return min(self.sides) + self.surface_area

    @property
    def volume(self):
        return self.length * self.width * self.height

    @property
    def face_perimeters(self):
        return [
            2 * (self.length + self.width),
            2 * (self.width + self.height),
            2 * (self.height + self.length),
        ]

    @property
    def ribbon_length(self):
        return min(self.face_perimeters) + self.volume


def read_input(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    presents = []
    for line in lines:
        length, width, height = [int(x) for x in line.split("x")]
        presents.append(Present(length, width, height))
    return presents

def compute_required_wrapping_paper(presents):
    total_wrapping_paper = 0
    for present in presents:
        total_wrapping_paper += present.wrapping_paper
    return total_wrapping_paper

def compute_required_ribbon(presents):
    total_ribbon = 0
    for present in presents:
        print(present, present.volume, present.ribbon_length)
        total_ribbon += present.ribbon_length
    return total_ribbon

if __name__ == "__main__":
    presents = read_input(sys.argv[1])
    wrapping_paper = compute_required_wrapping_paper(presents)
    print(wrapping_paper)

    test = [Present(2, 3, 4), Present(1,1,10)]
    ribbon = compute_required_ribbon(presents)
    print(ribbon)
