# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

# Warcraft III simulation.
# Weapons: sword (0), bomb (1), arrow (2).
# Warriors: dragon, ninja, iceman, lion, wolf.

WARRIOR_NAMES = ["dragon", "ninja", "iceman", "lion", "wolf"]


class Weapon:
    def __init__(self, w_type, usage):
        self.type = w_type
        self.usage = usage


class Warrior:
    def __init__(self, side, name, w_id, hp, atk, loyalty):
        self.side = side
        self.name = name
        self.id = w_id
        self.hp = hp
        self.atk = atk
        self.loyalty = loyalty
        self.weapons = []
        self.weapon_idx = 0

        # Initial weapon assignment logic based on warrior type and id.
        if name == 'dragon':
            self.weapons.append(Weapon(w_id % 3, 2 if w_id % 3 == 2 else 1))
        elif name == 'ninja':
            self.weapons.append(Weapon(w_id % 3, 2 if w_id % 3 == 2 else 1))
            self.weapons.append(Weapon((w_id + 1) % 3, 2 if (w_id + 1) % 3 == 2 else 1))
        elif name == 'iceman':
            self.weapons.append(Weapon(w_id % 3, 2 if w_id % 3 == 2 else 1))
        elif name == 'lion':
            self.weapons.append(Weapon(w_id % 3, 2 if w_id % 3 == 2 else 1))

    def sort_for_battle(self):
        # Battle sorting: ID ascending, Arrow usage ascending (used arrow 1 comes before new 2).
        self.weapons.sort(key=lambda x: (x.type, x.usage))

    def get_dmg(self, weapon):
        # Calculate weapon damage (floor values).
        if weapon.type == 0: return self.atk * 2 // 10
        if weapon.type == 1: return self.atk * 4 // 10
        if weapon.type == 2: return self.atk * 3 // 10
        return 0


class City:
    def __init__(self, pos):
        self.pos = pos
        self.red = None
        self.blue = None


def snatch(wolf, victim, time_p, pos):
    if not victim.weapons: return
    # Wolf steals all weapons of the smallest type available.
    min_type = min(w.type for w in victim.weapons)
    candidates = [w for w in victim.weapons if w.type == min_type]
    if min_type == 2:
        # If the smallest type is arrow, take new ones (usage 2) first.
        candidates.sort(key=lambda x: x.usage, reverse=True)

    taken = 0
    to_remove = []
    for w in candidates:
        if len(wolf.weapons) < 10:
            wolf.weapons.append(w)
            to_remove.append(w)
            taken += 1
    for w in to_remove:
        victim.weapons.remove(w)

    if taken > 0:
        w_name = ['sword', 'bomb', 'arrow'][min_type]
        print(
            f"{time_p}:35 {wolf.side} wolf {wolf.id} took {taken} {w_name} from {victim.side} {victim.name} {victim.id} in city {pos}")


def strike(attacker, defender):
    # Process a single attack with a weapon. Returns True if the weapon is consumed.
    w = attacker.weapons[attacker.weapon_idx]
    dmg = attacker.get_dmg(w)
    defender.hp -= dmg
    if w.type == 1:  # bomb
        if attacker.name != 'ninja':
            attacker.hp -= dmg // 2
        attacker.weapons.pop(attacker.weapon_idx)
        return True
    elif w.type == 2:  # arrow
        w.usage -= 1
        if w.usage == 0:
            attacker.weapons.pop(attacker.weapon_idx)
            return True
    return False


def loot(winner, loser):
    # Winner loots loser's weapons after killing them. Sorted by type, Arrow usage (new first).
    loser.weapons.sort(key=lambda x: (x.type, -x.usage))
    for w in loser.weapons:
        if len(winner.weapons) < 10:
            winner.weapons.append(w)


def conduct_battle(red, blue, time_p, pos):
    if not red.weapons and not blue.weapons:
        # Trivial draw if neither has weapons.
        print(f"{time_p}:40 both red {red.name} {red.id} and blue {blue.name} {blue.id} were alive in city {pos}")
        if red.name == 'dragon': print(f"{time_p}:40 red dragon {red.id} yelled in city {pos}")
        if blue.name == 'dragon': print(f"{time_p}:40 blue dragon {blue.id} yelled in city {pos}")
        return

    red.sort_for_battle()
    blue.sort_for_battle()
    red.weapon_idx, blue.weapon_idx = 0, 0
    p1, p2 = (red, blue) if pos % 2 != 0 else (blue, red)

    while True:
        if red.hp <= 0 or blue.hp <= 0: break
        state_pre = (red.hp, blue.hp, tuple((w.type, w.usage) for w in red.weapons),
                     tuple((w.type, w.usage) for w in blue.weapons), red.weapon_idx, blue.weapon_idx)

        # Attacker strikes
        if p1.weapons:
            removed = strike(p1, p2)
            if not removed: p1.weapon_idx += 1
            if p1.weapons:
                p1.weapon_idx %= len(p1.weapons)
            else:
                p1.weapon_idx = 0
        if red.hp <= 0 or blue.hp <= 0: break

        # Defender strikes back
        if p2.weapons:
            removed = strike(p2, p1)
            if not removed: p2.weapon_idx += 1
            if p2.weapons:
                p2.weapon_idx %= len(p2.weapons)
            else:
                p2.weapon_idx = 0
        if red.hp <= 0 or blue.hp <= 0: break

        # Detect if combat is making progress
        state_post = (red.hp, blue.hp, tuple((w.type, w.usage) for w in red.weapons),
                      tuple((w.type, w.usage) for w in blue.weapons), red.weapon_idx, blue.weapon_idx)
        if state_pre == state_post: break

    # Process battle results
    if red.hp <= 0 and blue.hp <= 0:
        print(f"{time_p}:40 both red {red.name} {red.id} and blue {blue.name} {blue.id} died in city {pos}")
    elif red.hp <= 0:
        loot(blue, red)
        print(
            f"{time_p}:40 blue {blue.name} {blue.id} killed red {red.name} {red.id} in city {pos} remaining {blue.hp} elements")
        if blue.name == 'dragon': print(f"{time_p}:40 blue dragon {blue.id} yelled in city {pos}")
    elif blue.hp <= 0:
        loot(red, blue)
        print(
            f"{time_p}:40 red {red.name} {red.id} killed blue {blue.name} {blue.id} in city {pos} remaining {red.hp} elements")
        if red.name == 'dragon': print(f"{time_p}:40 red dragon {red.id} yelled in city {pos}")
    else:
        print(f"{time_p}:40 both red {red.name} {red.id} and blue {blue.name} {blue.id} were alive in city {pos}")
        if red.name == 'dragon': print(f"{time_p}:40 red dragon {red.id} yelled in city {pos}")
        if blue.name == 'dragon': print(f"{time_p}:40 blue dragon {blue.id} yelled in city {pos}")


def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
    idx = 0
    num_test_cases = int(input_data[idx]);
    idx += 1

    for case_num in range(1, num_test_cases + 1):
        M, N, K, T = map(int, input_data[idx:idx + 4]);
        idx += 4
        hp_list = [int(input_data[idx + i]) for i in range(5)];
        idx += 5
        atk_list = [int(input_data[idx + i]) for i in range(5)];
        idx += 5
        hps = {WARRIOR_NAMES[i]: hp_list[i] for i in range(5)}
        atks = {WARRIOR_NAMES[i]: atk_list[i] for i in range(5)}
        red_order_names = ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
        blue_order_names = ['lion', 'dragon', 'ninja', 'iceman', 'wolf']
        cities = [City(i) for i in range(N + 2)]
        red_m, blue_m = M, M
        red_cnt, blue_cnt = 0, 0
        red_stopped, blue_stopped = False, False
        print(f"Case {case_num}:")

        for hour in range(T // 60 + 1):
            time_prefix = f"{hour:03d}"
            # :00 Born
            if not red_stopped:
                name = red_order_names[red_cnt % 5]
                if red_m >= hps[name]:
                    red_m -= hps[name]
                    red_cnt += 1
                    w = Warrior('red', name, red_cnt, hps[name], atks[name], red_m)
                    cities[0].red = w
                    print(f"{time_prefix}:00 red {name} {red_cnt} born")
                    if name == 'lion': print(f"Its loyalty is {w.loyalty}")
                else:
                    red_stopped = True
            if not blue_stopped:
                name = blue_order_names[blue_cnt % 5]
                if blue_m >= hps[name]:
                    blue_m -= hps[name]
                    blue_cnt += 1
                    w = Warrior('blue', name, blue_cnt, hps[name], atks[name], blue_m)
                    cities[N + 1].blue = w
                    print(f"{time_prefix}:00 blue {name} {blue_cnt} born")
                    if name == 'lion': print(f"Its loyalty is {w.loyalty}")
                else:
                    blue_stopped = True

            # :05 Escape
            if hour * 60 + 5 <= T:
                for i in range(N + 2):
                    if cities[i].red and cities[i].red.name == 'lion' and i <= N and cities[i].red.loyalty <= 0:
                        print(f"{time_prefix}:05 red lion {cities[i].red.id} ran away")
                        cities[i].red = None
                    if cities[i].blue and cities[i].blue.name == 'lion' and i >= 1 and cities[i].blue.loyalty <= 0:
                        print(f"{time_prefix}:05 blue lion {cities[i].blue.id} ran away")
                        cities[i].blue = None

            # :10 March
            is_captured = False
            if hour * 60 + 10 <= T:
                next_red, next_blue = [None] * (N + 2), [None] * (N + 2)
                for i in range(N + 1):
                    if cities[i].red:
                        w = cities[i].red
                        if w.name == 'iceman': w.hp -= w.hp // 10
                        if w.name == 'lion': w.loyalty -= K
                        next_red[i + 1] = w
                for i in range(1, N + 2):
                    if cities[i].blue:
                        w = cities[i].blue
                        if w.name == 'iceman': w.hp -= w.hp // 10
                        if w.name == 'lion': w.loyalty -= K
                        next_blue[i - 1] = w
                for i in range(N + 2):
                    cities[i].red, cities[i].blue = next_red[i], next_blue[i]
                for i in range(N + 2):
                    if i == 0 and cities[i].blue:
                        w = cities[i].blue
                        print(
                            f"{time_prefix}:10 blue {w.name} {w.id} reached red headquarter with {w.hp} elements and force {w.atk}")
                        print(f"{time_prefix}:10 red headquarter was taken")
                        is_captured = True
                    elif 1 <= i <= N:
                        if cities[i].red:
                            w = cities[i].red
                            print(
                                f"{time_prefix}:10 red {w.name} {w.id} marched to city {i} with {w.hp} elements and force {w.atk}")
                        if cities[i].blue:
                            w = cities[i].blue
                            print(
                                f"{time_prefix}:10 blue {w.name} {w.id} marched to city {i} with {w.hp} elements and force {w.atk}")
                    elif i == N + 1 and cities[i].red:
                        w = cities[i].red
                        print(
                            f"{time_prefix}:10 red {w.name} {w.id} reached blue headquarter with {w.hp} elements and force {w.atk}")
                        print(f"{time_prefix}:10 blue headquarter was taken")
                        is_captured = True
                if is_captured: break

            # :35 Snatch
            if hour * 60 + 35 <= T:
                for i in range(1, N + 1):
                    r, b = cities[i].red, cities[i].blue
                    if r and b:
                        if r.name == 'wolf' and b.name != 'wolf':
                            snatch(r, b, time_prefix, i)
                        elif b.name == 'wolf' and r.name != 'wolf':
                            snatch(b, r, time_prefix, i)

            # :40 Battle
            if hour * 60 + 40 <= T:
                for i in range(1, N + 1):
                    if cities[i].red and cities[i].blue:
                        conduct_battle(cities[i].red, cities[i].blue, time_prefix, i)
                        if cities[i].red and cities[i].red.hp <= 0: cities[i].red = None
                        if cities[i].blue and cities[i].blue.hp <= 0: cities[i].blue = None

            # :50 Report Headquarters
            if hour * 60 + 50 <= T:
                print(f"{time_prefix}:50 {red_m} elements in red headquarter")
                print(f"{time_prefix}:50 {blue_m} elements in blue headquarter")

            # :55 Status Report
            if hour * 60 + 55 <= T:
                for i in range(N + 2):
                    if cities[i].red:
                        w = cities[i].red
                        c = [0, 0, 0]
                        for wp in w.weapons: c[wp.type] += 1
                        print(
                            f"{time_prefix}:55 red {w.name} {w.id} has {c[0]} sword {c[1]} bomb {c[2]} arrow and {max(0, w.hp)} elements")
                    if cities[i].blue:
                        w = cities[i].blue
                        c = [0, 0, 0]
                        for wp in w.weapons: c[wp.type] += 1
                        print(
                            f"{time_prefix}:55 blue {w.name} {w.id} has {c[0]} sword {c[1]} bomb {c[2]} arrow and {max(0, w.hp)} elements")


if __name__ == '__main__':
    solve()
