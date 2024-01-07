import re
import sys

from dataclasses import dataclass
from enum import Enum
from typing import List


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def __lt__(self, other):
        return other is Shape.beats(self)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def beats(cls, shape):
        """
        Return the shape that beats the input.
        """
        _beats = {
            Shape.ROCK: Shape.PAPER,
            Shape.PAPER: Shape.SCISSORS,
            Shape.SCISSORS: Shape.ROCK,
        }
        return _beats[shape]

    @classmethod
    def loses_to(cls, shape):
        """
        Return the shape loses to the input.
        """
        _loses_to = {
            Shape.ROCK: Shape.SCISSORS,
            Shape.PAPER: Shape.ROCK,
            Shape.SCISSORS: Shape.PAPER,
        }
        return _loses_to[shape]

    @classmethod
    def from_string(cls, string: str) -> "Shape":
        match string:
            case "A" | "X":
                return cls.ROCK
            case "B" | "Y":
                return cls.PAPER
            case "C" | "Z":
                return cls.SCISSORS


@dataclass(frozen=True)
class Score:
    player1: int
    player2: int

    def __add__(self, other) -> "Score":
        return Score(
            self.player1 + other.player1,
            self.player2 + other.player2,
        )


@dataclass(frozen=True)
class Turn:
    player1: Shape
    player2: Shape

    @property
    def score(self) -> Score:
        # draw
        p1_score = self.player1.value
        p2_score = self.player2.value
        if self.player1 == self.player2:
            p1_score += 3
            p2_score += 3
        # p2 win
        elif self.player1 < self.player2:
            p2_score += 6
        # p1 win
        else:
            p1_score += 6
        return Score(p1_score, p2_score)


def read_input(file_name: str) -> List[str]:
    with open(file_name, "r") as f:
        return f.read().strip().splitlines()


def parse_turns(lines: List[str], full_instructions: bool) -> List[Turn]:
    """
    The player makes the assumption that XYZ map to shapes when not given
    the full instructions (Part 1). When the player has the full instructions,
    XYZ maps to lose/win/draw the round.
    """
    turns = []
    for line in lines:
        matches = re.findall(r"\b\w+\b", line)
        player1_shape = Shape.from_string(matches[0])
        if full_instructions:
            match matches[1]:
                case "X":
                    player2_shape = Shape.loses_to(player1_shape)
                case "Y":
                    player2_shape = player1_shape
                case "Z":
                    player2_shape = Shape.beats(player1_shape)
        else:
            player2_shape = Shape.from_string(matches[1])
        turns.append(Turn(player1_shape, player2_shape))
    return turns


def get_final_scores(turns: List[Turn]) -> Score:
    score = Score(0, 0)
    for turn in turns:
        score += turn.score
    return score


if __name__ == "__main__":
    lines = read_input(sys.argv[1])
    sequence = parse_turns(lines, False)
    final_scores = get_final_scores(sequence)
    print("Part 1:", final_scores.player2)

    sequence = parse_turns(lines, True)
    final_scores = get_final_scores(sequence)
    print("Part 2:", final_scores.player2)
