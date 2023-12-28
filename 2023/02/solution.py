from dataclasses import dataclass
from typing import List

@dataclass
class Draw:
    n_red: int
    n_blue: int
    n_green: int

@dataclass
class Game:
    id: int
    draws: List[Draw]

    def is_valid(self, rules):
        for draw in self.draws:
            if draw.n_red > rules.red_limit or draw.n_blue > rules.blue_limit or draw.n_green > rules.green_limit:
                return False
        return True

    def compute_power(self):
        max_red = 0
        max_blue = 0
        max_green = 0
        for draw in self.draws:
            max_red = max(max_red, draw.n_red)
            max_blue = max(max_blue, draw.n_blue)
            max_green = max(max_green, draw.n_green)
        return max_red * max_blue * max_green

@dataclass
class Rules:
    red_limit: int
    blue_limit: int
    green_limit: int

def read_games():
    games = []
    with open("input.txt", "r") as input:
        for line in input:
            game_txt, draws_txt = line.split(":")
            game_id = int(game_txt.split()[1])
            draws = read_draws(draws_txt)
            games.append(Game(game_id, draws))
    return games

def read_draws(text):
    draws = []
    for draw_txt in text.split(";"):
        n_red, n_blue, n_green = 0, 0, 0
        for color_txt in draw_txt.split(","):
            if "red" in color_txt:
                n_red += int(color_txt.split()[0])
            elif "blue" in color_txt:
                n_blue += int(color_txt.split()[0])
            elif "green" in color_txt:
                n_green += int(color_txt.split()[0])
        draws.append(Draw(n_red, n_blue, n_green))
    return draws


games = read_games()
part1_rules = Rules(red_limit=12, blue_limit=14, green_limit=13)
total = 0
for game in games:
    if game.is_valid(part1_rules):
        total += game.id
print(total)


power = 0
for game in games:
    power += game.compute_power()
print(power)