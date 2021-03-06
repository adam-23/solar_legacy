import random





def randomize_damage(damage):
    random_damage_multiplier = float(random.randint(80, 120) / 100)
    # print("random damage multiplier =", random_damage_multiplier)

    damage = (float(random_damage_multiplier * damage))
    # print("un-rounded float damage = ", damage_given)
    # Multiply by random number between .8 and 1.2
    damage = int(round(damage))
    # Round the damage after randomizing
    if damage == 0:
        damage = 1
        # Minimum attack damage is always 1
    # Check if alive after reduction
    # Print damage
    return damage


class Mob:
    """Base class, contains all main functions."""

    def __init__(self, name, vitality, strength, agility, defense, intelligence, spirit, magic_points):
        self.name = name
        # Name
        self.vitality = vitality
        # Hit points
        self.strength = strength
        # Physical damage
        self.agility = agility
        # Speed
        self.defense = defense
        # Flat physical reducer to damage
        self.intelligence = intelligence
        # Intelligence based magic defense and attack
        self.spirit = spirit
        # Spirit based magic defense and attack
        self.magic_points = magic_points
        # Magic points
        self.total_vitality = self.vitality
        # Max health, created when character is created.
        self.total_magic_points = self.magic_points
        # Max magic points

    is_alive = True
    # Determines if they can act or be acted on

    is_melee_target = True

    is_melee_attacker = True

    backRow = False
    # Can't be attacked with melee commands until front rows are killed
    # TODO remove one of these.
    # Melee or ranged damage
    is_defending = False

    def target_pick(self, target_list):
        # Print melee targets, only allow melee targets
        if self.is_melee_attacker:
            melee_targets = []
            for target in target_list:
                if target.is_melee_target:
                    melee_targets.append(target)
            target_list = melee_targets

        target_index = []
        final_pick = ""
        for target in target_list:
            target_index.append((target_list.index(target)) + 1)
            # Append the target index in order
            print(target.name, "=", target_index[target_list.index(target)])

            # Iterates through the list of target_lists and their indices.

        while_gate = False
        while not while_gate:
            try:
                chosen_target = int(input("Target : "))
            except ValueError:
                print("Not a valid target.")
                continue
            if chosen_target in target_index:
                final_pick = target_list[chosen_target - 1]
                # print("Target picked :", final_pick.name)
                break
            else:
                print("Not a valid target.")
                continue
        # Continuously ask the user for an input that matches an item in the index list

        print()
        return final_pick

    def check_life(self):
        # Check if alive

        if self.vitality <= 0:
            print(self.name + " is dead.")
            self.is_alive = False
            self.is_melee_target = False
            # If below, they die.

        """
        elif self.vitality > 0:
            print(self.name + " lives.")
            # If health is above zero, they live
        """

    def check_miss(self, target):
        target_evasion = float(target.agility / self.agility) * 4
        target_evasion += 5
        if target_evasion > 50:
            target_evasion = 50
        # Quotient of agility times 4, + 5, no bigger than 50
        evasion_chance = random.randint(0, 101)
        # Pick a random number.
        if target_evasion >= evasion_chance:
            print(self.name, "missed", target.name + "!\n")
            return True
            # If evasion is higher than random number, end the attack.

    def single_hit(self, target):
        damage = (self.strength * 2) - target.defense
        # Damage is 2 * strength minus target defense
        return damage

    def check_hits(self):
        hits = float(self.agility / 8)
        # Hits are agility / 8
        hits = int(round(hits))
        # Round hits to a whole number
        if hits < 1:
            hits = 1
            # Always attack at least once
        return hits

    def reduce_vitality(self, target, damage):
        target.vitality -= damage
        # Reduce target vitality
        if target.vitality < 0:
            target.vitality = 0
            # If vitality is below 0, assign it 0
        print(self.name, "dealt " + str(damage), "damage!")
        print(target.name, "HP :", str(target.vitality) + "/" + str(target.total_vitality))
        return target.vitality
        # Print target, hits, damage, target health

    def defend(self):
        self.is_defending = True
        return self.is_defending

    def attack(self, target):

        """
        1. Check life
        2. Hit or miss
        3. Determine number of hits
        4. Determine damage individually per hit
        5. Deal total damage from hits
        6. Print all information
        7. Close and return all info
        """
        total_damage_given = 0
        # Place holder variable for damage
        """if not target.is_melee_target:
            print(target.name, "is not a melee target.")
            return"""

        if self.is_alive:
            # Check if target and attacker are both alive, else attack is cancelled.

            miss = self.check_miss(target)
            if miss:
                return
            # Check if hit or miss

            hits_number = self.check_hits()
            # Hits number is the number of hits calculated.

            for i in range(0, hits_number):
                # For every hit,
                damage_given = self.single_hit(target)
                damage_given = randomize_damage(damage_given)
                total_damage_given += damage_given
                # Calculate damage per hit, randomize damage, add to total

            print(self.name, "attacked", target.name + "!")
            if target.is_defending:
                print(target.name, "is defending!")
                total_damage_given = int(round(total_damage_given * 0.6))
                # If target is defending, reduce total damage by 40% and then round up.
            print(self.name + " dealt " + str(hits_number) + " hits!")
            # Print summary of hits

            self.reduce_vitality(target, total_damage_given)
            # Reduce target vitality, print damage, print target vitality.

            target.check_life()
            # Check if target is dead. If so, mark them as such.
            print()
        else:
            print("One is dead, attack cancelled.")
            # If target or attacker is dead, stop.
            return

    def special_command(self, target):
        specialty_name = "[Rush]"
        print(specialty_name)
        self.strength *= 1.5
        self.attack(target)
        self.strength *= (2 / 3)

    # TODO: battle commands for every character

    def battle_command_list(self, target):
        active_battle = True
        print("Attack = A")
        print("Defend = D")
        # print("Item = I")
        # print("Run = R")
        # print("Tap = T")
        print("S for special command")
        while active_battle:
            print()
            self.is_defending = False
            # If they try to act, they can no longer be actively defending.
            try:
                user_choice = input("Pick a command:  ").lower()
                print()
            except TypeError or ValueError:
                continue
            if user_choice == 'a':
                attack_target = self.target_pick(target)
                self.attack(attack_target)
            elif user_choice == 'd':
                self.defend()
            elif user_choice == 's':
                print()
                # TODO Run Special user commands:
                # special_command(self.specialty_name, target)
            """elif user_choice == 'i':
                # TODO use_item
                print()
            elif user_choice == 'r':
                # TODO run_away()
                print()"""

    # TODO MP regeneration after every battle, action
    # TODO Row system