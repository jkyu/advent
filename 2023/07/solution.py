import sys

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import List

class Card(Enum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1

    def __lt__(self, other):
        return self.value < other.value

    @staticmethod
    def from_string(card_string: str, with_jokers=False):
        mapping = {
            "A": Card.ACE,
            "K": Card.KING,
            "Q": Card.QUEEN,
            "J": Card.JACK,
            "T": Card.TEN,
            "9": Card.NINE,
            "8": Card.EIGHT,
            "7": Card.SEVEN,
            "6": Card.SIX,
            "5": Card.FIVE,
            "4": Card.FOUR,
            "3": Card.THREE,
            "2": Card.TWO,
        }
        if with_jokers:
            mapping["J"] = Card.JOKER
        return mapping[card_string]


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    def __lt__(self, other):
        return self.value < other.value

    @staticmethod
    def from_cards(cards: List[Card], with_jokers=False):
        # map of card to multiplicities
        counter = Counter(cards)
        # if there are jokers, add all of the jokers into the most populous card
        # also make sure there are not ONLY jokers
        if with_jokers and Card.JOKER in counter and len(counter) > 1:
            num_jokers = counter.pop(Card.JOKER)
            card_counts = [(count, card) for card, count in counter.items()]
            card_counts.sort(key=lambda x: x[0]) # sort by count
            # add the jokers to the card with the highest count
            counter[card_counts[-1][1]] += num_jokers
        # set of count multiplicities
        multiplicities = set(counter.values())
        unique_cards = len(counter)
        # only one card: must be five of a kind
        if unique_cards == 1:
            return HandType.FIVE_OF_A_KIND
        # two unique cards: can be full house or four of a kind
        elif unique_cards == 2:
            if 4 in multiplicities:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE
        # three unique cards: can be two pairs or three of a kind
        elif unique_cards == 3:
            if 3 in multiplicities:
                return HandType.THREE_OF_A_KIND
            else:
                return HandType.TWO_PAIR
        # four unique cards: can only be one pair
        elif unique_cards == 4:
            return HandType.ONE_PAIR
        # five unique cards: high card
        else:
            return HandType.HIGH_CARD


@dataclass
class Hand:
    card_string: str
    cards: List[Card]
    hand_type: HandType
    bid: int

    def __lt__(self, other):
        # hand type takes precedence in comparison
        if self.hand_type < other.hand_type:
            return True
        # if same hand type, compare cards from first to last
        elif self.hand_type == other.hand_type:
            for i in range(len(self.cards)):
                # immediately return if card is smaller
                if self.cards[i] < other.cards[i]:
                    return True
                # continue iterating if cards are equivalent
                elif self.cards[i] == other.cards[i]:
                    continue
                # immediately return if card is larger
                else:
                    return False
            # if we reach the end, we had identical hands
            return False
        # otherwise, not less than other hand
        else:
            return False

    def __eq__(self, other):
        if self.hand_type != other.hand_type:
            return False
        else:
            for i in range(len(self.cards)):
                if self.cards[i] != other.cards[i]:
                    return False
            return True


def read_file(input: str):
    with open(input) as f:
        text = f.read().strip()
        lines = text.split("\n")
    return lines

def convert_lines_to_cards(lines: List[str], with_jokers=False):
    hands = []
    for line in lines:
        card_txt, bid_txt = line.split()
        cards = [Card.from_string(x, with_jokers) for x in list(card_txt)]
        hand_type = HandType.from_cards(cards, with_jokers)
        bid = int(bid_txt)
        hands.append(Hand(card_txt, cards, hand_type, bid))
    return hands

def rank_hands_and_compute_winnings(hands: List[Hand]):
    hands.sort()
    winnings = 0
    for i, hand in enumerate(hands):
        winnings += (i+1) * hand.bid
    return winnings

if __name__ == "__main__":
    txt_lines = read_file(sys.argv[1])
    hands = convert_lines_to_cards(txt_lines)
    winnings1 = rank_hands_and_compute_winnings(hands)
    print(winnings1)

    hands = convert_lines_to_cards(txt_lines, with_jokers=True)
    winnings2 = rank_hands_and_compute_winnings(hands)
    print(winnings2)