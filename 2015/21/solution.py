import re
import sys

from dataclasses import dataclass

@dataclass(frozen=True)
class Character:
    hp: int
    damage: int
    armor: int

    def equip_item(self, item):
        damage = self.damage + item.damage
        armor = self.armor + item.armor
        return Character(self.hp, damage, armor)

@dataclass(frozen=True)
class Item:
    cost: int
    damage: int
    armor: int

def read_boss_stats(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    stats = [int(re.findall(r'\d+', line)[0]) for line in lines]
    return Character(*stats)

def lines_to_items(lines):
    items = []
    for line in lines:
        # use a negative lookbehind to avoid number 
        # sequences that start with a + sign
        stats = re.findall(r'(?<!\+)\b\d+\b', line)
        items.append(Item(int(stats[0]), int(stats[1]), int(stats[2])))
    return items

def read_shop(file):
    with open(file, "r") as f:
        weapon_txt, armor_txt, ring_txt = f.read().strip().split("\n\n")
    weapons = lines_to_items(weapon_txt.splitlines()[1:])
    armors = lines_to_items(armor_txt.splitlines()[1:])
    rings = lines_to_items(ring_txt.splitlines()[1:])
    return weapons, armors, rings

def can_player_win(player, equipment, boss):
    """
    Compute the damage taken and dealt per turn by the player
    after equipping all purchased items. Then compute the number
    of turns that the player needs to deplete the hit points
    of the boss and the number of turns the boss needs to deplete
    the player's hit points. Since the player goes first, if the
    turns required are equal, the player will win. If fewer turns
    are required to deplete the boss's hit points, the player wins.
    """
    for item in equipment:
        player = player.equip_item(item)
    damage_dealt_per_turn = max(player.damage - boss.armor, 1)
    damage_taken_per_turn = max(boss.damage - player.armor, 1)
    turns_to_win = (boss.hp // damage_dealt_per_turn)
    if boss.hp % damage_dealt_per_turn > 0:
        turns_to_win += 1
    turns_to_lose = (player.hp // damage_taken_per_turn)
    if player.hp % damage_taken_per_turn > 0:
        turns_to_lose += 1
    # player attacks first, so tie goes to player
    if turns_to_win <= turns_to_lose:
        return True
    else:
        return False

def least_gold_to_win(player, boss, weapons, armors, rings):
    """
    Brute force sampling of all equipment combinations obeying
    1 weapon, 0-1 armors, 0-2 rings. A dummy armor and two 
    dummy rings are included in order to generate all equipment
    combinations in one block.
    """
    gold = sys.maxsize
    for weapon in weapons:
        for armor in armors:
            for i in range(len(rings)):
                for j in range(i+1, len(rings)):
                    equipment = [weapon, armor, rings[i], rings[j]]
                    if can_player_win(player, equipment, boss):
                        cost = sum(map(lambda item: item.cost, equipment))
                        gold = min(gold, cost)
    return gold

def most_gold_to_lose(player, boss, weapons, armors, rings):
    gold = -sys.maxsize
    for weapon in weapons:
        for armor in armors:
            for i in range(len(rings)):
                for j in range(i+1, len(rings)):
                    equipment = [weapon, armor, rings[i], rings[j]]
                    if not can_player_win(player, equipment, boss):
                        cost = sum(map(lambda item: item.cost, equipment))
                        gold = max(gold, cost)
    return gold

if __name__ == "__main__":
    boss = read_boss_stats(sys.argv[1])
    player = Character(100, 0, 0)

    weapons, armors, rings = read_shop(sys.argv[2])
    # armor is optional. add an empty armor to represent that choice
    armors.append(Item(0, 0, 0))
    # rings are optional up to 2. add two empty rings.
    rings.append(Item(0, 0, 0))
    rings.append(Item(0, 0, 0))

    gold = least_gold_to_win(player, boss, weapons, armors, rings)
    print(gold)

    gold = most_gold_to_lose(player, boss, weapons, armors, rings)
    print(gold)