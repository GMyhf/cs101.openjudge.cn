# T-004-r5 参考实现：人提供的平台 Accepted 版本（2026-07-26 替换）
# 原自写实现平台判 Wrong Answer，生成的数据是错的。
import sys
from dataclasses import dataclass

# 兵种编号：
# 0 dragon
# 1 ninja
# 2 iceman
# 3 lion
# 4 wolf
NAMES = ["dragon", "ninja", "iceman", "lion", "wolf"]

RED_ORDER = [2, 3, 4, 1, 0]
BLUE_ORDER = [3, 0, 1, 2, 4]

@dataclass
class Warrior:
    side: str
    kind: int
    number: int
    hp: int
    attack: int
    position: int

    steps: int = 0
    wolf_kills: int = 0
    alive: bool = True
    reached: bool = False

class Headquarter:
    def __init__(self, side, elements, position):
        self.side = side
        self.elements = elements
        self.position = position
        self.next_index = 0
        self.warrior_count = 0
        self.invaders = 0

class City:
    def __init__(self):
        self.elements = 0
        self.flag = None
        self.last_winner = None

class World:
    def __init__(self, initial_elements, city_count, time_limit,
                 initial_hp, initial_attack):
        self.n = city_count
        self.time_limit = time_limit
        self.initial_hp = initial_hp
        self.initial_attack = initial_attack
        self.cities = [City() for _ in range(self.n + 1)]
        self.headquarters = {
            "red": Headquarter("red", initial_elements, 0),
            "blue": Headquarter("blue", initial_elements, self.n + 1)
        }
        self.warriors = []
        self.answer = []
        self.war_ended = False

    @staticmethod
    def format_time(current_time):
        hour = current_time // 60
        minute = current_time % 60
        return f"{hour:03d}:{minute:02d}"

    @staticmethod
    def warrior_name(warrior):
        return (
            f"{warrior.side} "
            f"{NAMES[warrior.kind]} "
            f"{warrior.number}"
        )

    def create_warrior(self, current_time, side):
        hq = self.headquarters[side]
        order = RED_ORDER if side == "red" else BLUE_ORDER
        kind = order[hq.next_index]
        cost = self.initial_hp[kind]
        if hq.elements < cost:
            return
        hq.elements -= cost
        hq.warrior_count += 1
        warrior = Warrior(
            side=side,
            kind=kind,
            number=hq.warrior_count,
            hp=self.initial_hp[kind],
            attack=self.initial_attack[kind],
            position=hq.position
        )
        self.warriors.append(warrior)
        hq.next_index = (hq.next_index + 1) % 5
        self.answer.append(
            f"{self.format_time(current_time)} "
            f"{self.warrior_name(warrior)} born"
        )

    def march(self, current_time):
        moved = []
        for warrior in self.warriors:
            if not warrior.alive or warrior.reached:
                continue
            if warrior.side == "red":
                warrior.position += 1
            else:
                warrior.position -= 1
            warrior.steps += 1
            if warrior.kind == 2 and warrior.steps % 2 == 0:
                warrior.hp = max(1, warrior.hp - 9)
                warrior.attack += 20
            reached_enemy_hq = (
                warrior.side == "red"
                and warrior.position == self.n + 1
            ) or (
                warrior.side == "blue"
                and warrior.position == 0
            )
            if reached_enemy_hq:
                warrior.reached = True
                enemy_side = (
                    "blue" if warrior.side == "red" else "red"
                )
                self.headquarters[enemy_side].invaders += 1
            moved.append(warrior)

        moved_by_position = {}
        for warrior in moved:
            moved_by_position.setdefault(
                warrior.position, []
            ).append(warrior)

        captured = False
        for position in range(self.n + 2):
            group = moved_by_position.get(position, [])
            group.sort(
                key=lambda warrior:
                0 if warrior.side == "red" else 1
            )
            for warrior in group:
                if position == 0 or position == self.n + 1:
                    enemy_side = (
                        "blue"
                        if warrior.side == "red"
                        else "red"
                    )
                    self.answer.append(
                        f"{self.format_time(current_time)} "
                        f"{self.warrior_name(warrior)} reached "
                        f"{enemy_side} headquarter with "
                        f"{warrior.hp} elements and force "
                        f"{warrior.attack}"
                    )
                else:
                    self.answer.append(
                        f"{self.format_time(current_time)} "
                        f"{self.warrior_name(warrior)} marched "
                        f"to city {position} with "
                        f"{warrior.hp} elements and force "
                        f"{warrior.attack}"
                    )
            if (
                position == 0
                and self.headquarters["red"].invaders >= 2
            ):
                self.answer.append(
                    f"{self.format_time(current_time)} "
                    f"red headquarter was taken"
                )
                captured = True
            if (
                position == self.n + 1
                and self.headquarters["blue"].invaders >= 2
            ):
                self.answer.append(
                    f"{self.format_time(current_time)} "
                    f"blue headquarter was taken"
                )
                captured = True
        self.war_ended = captured

    def get_city_warriors(self, city_number):
        red_warrior = None
        blue_warrior = None
        for warrior in self.warriors:
            if (
                warrior.alive
                and not warrior.reached
                and warrior.position == city_number
            ):
                if warrior.side == "red":
                    red_warrior = warrior
                else:
                    blue_warrior = warrior
        return red_warrior, blue_warrior

    def collect_city_elements(self, current_time):
        for city_number in range(1, self.n + 1):
            red_warrior, blue_warrior = self.get_city_warriors(
                city_number
            )
            if (red_warrior is None) != (blue_warrior is None):
                warrior = (
                    red_warrior
                    if red_warrior is not None
                    else blue_warrior
                )
                amount = self.cities[city_number].elements
                if amount > 0:
                    self.headquarters[warrior.side].elements += amount
                    self.cities[city_number].elements = 0
                    self.answer.append(
                        f"{self.format_time(current_time)} "
                        f"{self.warrior_name(warrior)} earned "
                        f"{amount} elements for his headquarter"
                    )

    def battle(self, current_time):
        battle_records = []
        winners = {
            "red": [],
            "blue": []
        }
        for city_number in range(1, self.n + 1):
            red_warrior, blue_warrior = self.get_city_warriors(
                city_number
            )
            if red_warrior is None or blue_warrior is None:
                continue
            city = self.cities[city_number]
            red_attacks = (
                city.flag == "red"
                or (
                    city.flag is None
                    and city_number % 2 == 1
                )
            )
            if red_attacks:
                attacker = red_warrior
                defender = blue_warrior
            else:
                attacker = blue_warrior
                defender = red_warrior
            logs = []
            logs.append(
                f"{self.format_time(current_time)} "
                f"{self.warrior_name(attacker)} attacked "
                f"{self.warrior_name(defender)} in city "
                f"{city_number} with {attacker.hp} elements "
                f"and force {attacker.attack}"
            )
            attacker_lion_hp = attacker.hp
            defender_lion_hp = defender.hp
            winner = None
            defender.hp -= attacker.attack
            if defender.hp <= 0:
                defender.alive = False
                logs.append(
                    f"{self.format_time(current_time)} "
                    f"{self.warrior_name(defender)} was killed "
                    f"in city {city_number}"
                )
                winner = attacker
                if attacker.kind == 4:
                    attacker.wolf_kills += 1
                    if attacker.wolf_kills % 2 == 0:
                        attacker.hp *= 2
                        attacker.attack *= 2
                if defender.kind == 3:
                    attacker.hp += defender_lion_hp
            else:
                if defender.kind != 1:
                    logs.append(
                        f"{self.format_time(current_time)} "
                        f"{self.warrior_name(defender)} fought "
                        f"back against "
                        f"{self.warrior_name(attacker)} "
                        f"in city {city_number}"
                    )
                    attacker.hp -= defender.attack // 2
                    if attacker.hp <= 0:
                        attacker.alive = False
                        logs.append(
                            f"{self.format_time(current_time)} "
                            f"{self.warrior_name(attacker)} "
                            f"was killed in city {city_number}"
                        )
                        winner = defender
                        if attacker.kind == 3:
                            defender.hp += attacker_lion_hp
            if attacker.kind == 0 and attacker.alive:
                logs.append(
                    f"{self.format_time(current_time)} "
                    f"{self.warrior_name(attacker)} yelled "
                    f"in city {city_number}"
                )
            flag_log = None
            if winner is not None:
                side = winner.side
                winners[side].append((city_number, winner))
                if (
                    city.last_winner == side
                    and city.flag != side
                ):
                    city.flag = side
                    flag_log = (
                        f"{self.format_time(current_time)} "
                        f"{side} flag raised in city "
                        f"{city_number}"
                    )
                city.last_winner = side
            else:
                city.last_winner = None
            battle_records.append(
                (
                    city_number,
                    logs,
                    winner,
                    city.elements,
                    flag_log
                )
            )

        for city_number, warrior in sorted(
            winners["red"],
            key=lambda item: -item[0]
        ):
            red_hq = self.headquarters["red"]
            if red_hq.elements >= 8:
                red_hq.elements -= 8
                warrior.hp += 8

        for city_number, warrior in sorted(
            winners["blue"],
            key=lambda item: item[0]
        ):
            blue_hq = self.headquarters["blue"]
            if blue_hq.elements >= 8:
                blue_hq.elements -= 8
                warrior.hp += 8

        for (
            city_number,
            logs,
            winner,
            amount,
            flag_log
        ) in battle_records:
            if winner is not None:
                self.headquarters[winner.side].elements += amount
                self.cities[city_number].elements = 0

        for (
            city_number,
            logs,
            winner,
            amount,
            flag_log
        ) in battle_records:
            self.answer.extend(logs)
            if winner is not None:
                self.answer.append(
                    f"{self.format_time(current_time)} "
                    f"{self.warrior_name(winner)} earned "
                    f"{amount} elements for his headquarter"
                )
            if flag_log is not None:
                self.answer.append(flag_log)

    def simulate(self):
        for current_time in range(self.time_limit + 1):
            if self.war_ended:
                break
            minute = current_time % 60
            if minute == 0:
                self.create_warrior(current_time, "red")
                self.create_warrior(current_time, "blue")
            elif minute == 10:
                self.march(current_time)
            elif minute == 20:
                for city_number in range(1, self.n + 1):
                    self.cities[city_number].elements += 10
            elif minute == 30:
                self.collect_city_elements(current_time)
            elif minute == 40:
                self.battle(current_time)
            elif minute == 50:
                red_elements = self.headquarters["red"].elements
                blue_elements = self.headquarters["blue"].elements
                self.answer.append(
                    f"{self.format_time(current_time)} "
                    f"{red_elements} elements in red headquarter"
                )
                self.answer.append(
                    f"{self.format_time(current_time)} "
                    f"{blue_elements} elements in blue headquarter"
                )
        return self.answer

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    iterator = iter(data)
    case_count = next(iterator)
    output = []
    for case_number in range(1, case_count + 1):
        initial_elements = next(iterator)
        city_count = next(iterator)
        time_limit = next(iterator)
        initial_hp = [next(iterator) for _ in range(5)]
        initial_attack = [next(iterator) for _ in range(5)]
        world = World(
            initial_elements,
            city_count,
            time_limit,
            initial_hp,
            initial_attack
        )
        output.append(f"Case:{case_number}")
        output.extend(world.simulate())
    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
