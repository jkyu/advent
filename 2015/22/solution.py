import copy

from queue import PriorityQueue

class Character:
    """Base class for game characters"""
    def __init__(self, hp: int):
        self.hp = hp
        self.armor = 0

    def take_damage(self, points: int):
        self.hp -= max(1, points - self.armor)

    @property
    def is_defeated(self):
        return self.hp <= 0

    def __repr__(self):
        return f"Character(hp={self.hp})"

class Spell:
    """Base class for spells"""
    name = "spell"
    cost = 0
    duration = 0
    damage = 0
    armor_bonus = 0
    mana_recovery = 0
    tick_rate = 1

    def __init__(self):
        self.duration = self.__class__.duration
    
    def cast(self, caster: Character, target: Character):
        """Perform instant effect of spell"""
        pass

    def tick(self, caster: Character, target: Character):
        """Perform persistent spell effect and tick down timer"""
        pass

    def expire(self, caster: Character):
        """Perform (or undo) spell upon timer expiration"""
        pass

    @property
    def should_expire(self):
        return self.duration == 0

    def __repr__(self):
        parts = [
            f"{self.__class__.__name__}(",
            f"cost={self.cost},",
            f"duration={self.duration},",
            f"damage={self.damage},",
            f"armor_bonus={self.armor_bonus},",
            f"mana_recovery={self.mana_recovery},",
            f"tick_rate={self.tick_rate})"
        ]
        return " ".join(parts)

class Boss(Character):
    def __init__(self, hp: int, damage: int):
        super().__init__(hp)
        self.damage = damage

    def attack(self, target: Character):
        target.take_damage(self.damage)

    def __repr__(self):
        return f"Boss(hp={self.hp}, damage={self.damage})"

class Player(Character):
    def __init__(self, hp: int, mana: int):
        super().__init__(hp)
        self.mana = mana
        self.mana_spent = 0
        self.spells = {}

    def recover_mana(self, points: int):
        self.mana += points

    def modify_armor(self, points: int):
        self.armor += points

    def heal(self, points: int):
        self.hp += points

    def tick_spells(self, target: Character):
        """
        All spells perform their persistent effects
        and the duration timer ticks down. If the 
        duration timer becomes zero, remove the spell
        from the player's current list of effects.
        """
        expired = set()
        for name, spell in self.spells.items():
            spell.tick(self, target)
            if spell.should_expire:
                spell.expire(self)
                expired.add(name)
        for name in expired:
            self.spells.pop(name)

    def cast_spell(self, target: Character, spell: Spell):
        """
        Perform the spell's immediate cast action,
        which in some cases might be nothing. If the
        spell has a duration, store to allow it to
        perform persistent effects and tick down over
        subsequent turns.
        """
        self.mana -= spell.cost
        self.mana_spent += spell.cost
        spell.cast(self, target)
        if spell.duration > 0:
            self.spells[spell.name] = spell

    def spell_unavailable(self, spell: Spell):
        """
        A spell that is still ongoing cannot be cast
        again until it expires.
        """
        return spell.name in self.spells

    def __repr__(self):
        parts = [
            f"Player(hp={self.hp},",
            f"mana={self.mana},",
            f"mana_spent={self.mana_spent},",
            f"armor={self.armor},",
            f"spells={self.spells})",
        ]
        return " ".join(parts)

class MagicMissile(Spell):
    """
    Magic Missile only has an immediate effect on cast.
    """
    name = "Magic Missile"
    cost = 53
    damage = 4

    def cast(self, caster: Character, target: Character):
        target.take_damage(self.damage)

class Drain(Spell):
    """
    Drain only has an immediate effect on cast.
    """
    name = "Drain"
    cost = 73
    damage = 2

    def cast(self, caster: Character, target: Character):
        target.take_damage(self.damage)
        caster.heal(self.damage)

class Shield(Spell):
    """
    Shield grants a bonus on cast and removes it
    on expiration. It is a persistent spell, so
    its duration ticks down each turn.
    """
    name = "Shield"
    cost = 113
    duration = 6
    armor_bonus = 7

    def cast(self, caster: Character, target: Character):
        caster.modify_armor(self.armor_bonus)

    def tick(self, caster: Character, target: Character):
        self.duration -= self.tick_rate

    def expire(self, caster: Character):
        caster.modify_armor(-self.armor_bonus)

class Poison(Spell):
    """
    Poison does nothing on cast and expiration.
    It only applies a persistent effect.
    """
    name = "Poison"
    cost = 173
    duration = 6
    damage = 3

    def tick(self, caster: Character, target: Character):
        target.take_damage(self.damage)
        self.duration -= self.tick_rate

class Recharge(Spell):
    """
    Recharge does nothing on cast and expiration.
    It only applies a persistent effect.
    """
    name = "Recharge"
    cost = 229
    duration = 5
    mana_recovery = 101

    def tick(self, caster: Character, target: Character):
        caster.recover_mana(self.mana_recovery)
        self.duration -= self.tick_rate

class State:
    def __init__(self, player: Character, boss: Character):
        self.player = player
        self.boss = boss

    def __lt__(self, other: "State"):
        return self.player.mana_spent < other.player.mana_spent

    def __repr__(self):
        return f"State(player={self.player}, boss={self.boss})"

def find_win_with_lowest_mana_cost(
        player: Player,
        boss: Boss,
        hard_mode: bool = False
    ) -> State:
    """
    Use Dijkstra's algorithm to find the win that requires the
    least mana expense by the player.

    Order of events:
    - if hard mode, player takes one damage
    - apply any persistent effects, such as poison damage or 
      mana recovery. also tick down timers on any persistent
      spells
    - player takes turn and can cast spells that are not already
      in effect
    - boss attacks the player
    """
    # this is the wizard's spellbook containing spells that have
    # their full durations
    spellbook = [MagicMissile(), Drain(), Shield(), Poison(), Recharge()]

    state = State(player, boss)
    heap = PriorityQueue()
    heap.put(state)

    while not heap.empty():
        state = heap.get()
        # clone the characters to avoid modifying other game states
        player = copy.deepcopy(state.player)
        boss = copy.deepcopy(state.boss)

        # check for lowest cost boss defeat
        if boss.is_defeated:
            return state

        if hard_mode:
            player.take_damage(1)

        # if player was defeated, toss this game state
        if player.is_defeated:
            continue

        # tick active spells
        # spells can expire and then be recast immediately!
        # stuff like mana recovery or damage ticks happen here
        player.tick_spells(boss)

        # try out each spell
        for spell in spellbook:
            # lose if cannot cast any spells
            if player.mana < spell.cost:
                continue
            else:
                # activate the spell for casting
                spell = copy.deepcopy(spell)

            # spell has not completed, so do not recast it
            if player.spell_unavailable(spell):
                continue

            # clone the characters to avoid modifying other game states
            new_player = copy.deepcopy(player)
            new_boss = copy.deepcopy(boss)

            # player action
            new_player.cast_spell(new_boss, spell)

            # boss action
            new_player.tick_spells(new_boss)
            new_boss.attack(new_player)

            # put new game state in the heap
            new_state = State(new_player, new_boss)
            heap.put(new_state)

if __name__ == "__main__":
    boss = Boss(51, 9)
    player = Player(50, 500)
    state = find_win_with_lowest_mana_cost(player, boss)
    print(state.player.mana_spent)

    state = find_win_with_lowest_mana_cost(player, boss, True)
    print(state.player.mana_spent)
