from dataclasses import dataclass
from typing import Set

@dataclass
class Card:
    card_id: int
    winning_numbers: Set[int]
    my_numbers: Set[int]

    @property
    def n_matches(self):
        matched_numbers = self.winning_numbers.intersection(self.my_numbers)
        return len(matched_numbers)

    @property
    def points(self):
        n_matches = self.n_matches
        if n_matches == 0:
            return 0
        else:
            return 2 ** (n_matches-1)

def read_card(filename):
    cards = []
    with open(filename, "r") as f:
        for line in f:
            card_label, numbers = line.strip().split(":")
            card_id = int(card_label.split()[1])
            winning_numbers_txt, my_numbers_txt = numbers.split("|")
            winning_numbers = set(int(x) for x in winning_numbers_txt.split())
            my_numbers = set(int(x) for x in my_numbers_txt.split())
            card = Card(card_id, winning_numbers, my_numbers)
            cards.append(card)
    return cards

def compute_total_points(cards):
    points = 0
    for card in cards:
        points += card.points
    return points

def compute_number_of_total_scratchcards(cards):
    card_multiplicity = [1] * len(cards)
    for i, card in enumerate(cards):
        for j in range(card.n_matches):
            if i+j+1 >= len(cards):
                break
            card_multiplicity[i+j+1] += card_multiplicity[i]
    return sum(card_multiplicity)

if __name__=="__main__":
    cards = read_card("input.txt")
    print(compute_total_points(cards))
    print(compute_number_of_total_scratchcards(cards))