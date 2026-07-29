# External reference: http://cs101.openjudge.cn/practice/03141/statistics/
# Accepted submission: 52723797
# Source: http://cs101.openjudge.cn/practice/solution/52723797/
# License: not declared on the submission page; no license is inferred.

# 武器编号 -> 名称映射
WEAPON = {0: "sword", 1: "bomb", 2: "arrow"}
# 武士名称 -> 索引映射（对应输入的5个生命值）
NAME2IDX = {"dragon": 0, "ninja": 1, "iceman": 2, "lion": 3, "wolf": 4}
# 红蓝方制造顺序
RED_ORDER = ["iceman", "lion", "wolf", "ninja", "dragon"]
BLUE_ORDER = ["lion", "dragon", "ninja", "iceman", "wolf"]


class Headquarter:
    """司令部类，封装所有状态和制造逻辑"""
    def __init__(self, color, init_hp, hp_list):
        self.color = color          # red / blue
        self.hp = init_hp           # 当前生命元
        self.hp_list = hp_list      # 5种武士的初始生命值
        self.stopped = False        # 是否停止制造
        self.ptr = 0                # 制造顺序指针
        self.warrior_id = 0         # 武士编号（自增）
        self.cnt = [0] * 5         # 武士计数：[dragon, ninja, iceman, lion, wolf]
        # 制造顺序
        self.order = RED_ORDER if color == "red" else BLUE_ORDER

    def try_make(self):
        """尝试制造武士，返回(是否成功, 武士名称, 编号, 生命值, 剩余生命元)"""
        if self.stopped:
            return (False, "", 0, 0, 0)

        # 遍历5种武士，尝试制造
        for _ in range(5):
            name = self.order[self.ptr]
            idx = NAME2IDX[name]
            cost = self.hp_list[idx]

            if self.hp >= cost:
                # 可以制造：扣除生命元，编号+1，计数+1
                self.hp -= cost
                self.warrior_id += 1
                self.cnt[idx] += 1
                res = (True, name, self.warrior_id, cost, self.hp)
                # 指针后移（循环）
                self.ptr = (self.ptr + 1) % 5
                return res

            # 不足，尝试下一个
            self.ptr = (self.ptr + 1) % 5

        # 所有都无法制造，停止
        self.stopped = True
        return (False, "", 0, 0, 0)


def print_warrior_extra(name, wid, remain_hp, cost_hp):
    """打印武士的额外属性信息"""
    if name == "dragon":
        w = WEAPON[wid % 3]
        morale = remain_hp / cost_hp
        print(f"It has a {w},and it's morale is {morale:.2f}")
    elif name == "ninja":
        w1 = WEAPON[wid % 3]
        w2 = WEAPON[(wid + 1) % 3]
        print(f"It has a {w1} and a {w2}")
    elif name == "iceman":
        w = WEAPON[wid % 3]
        print(f"It has a {w}")
    elif name == "lion":
        print(f"It's loyalty is {remain_hp}")
    # wolf 无额外信息


def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    case_num = int(input[ptr])
    ptr += 1

    for case in range(1, case_num + 1):
        print(f"Case:{case}")
        M = int(input[ptr])
        ptr += 1
        # 读取5种武士生命值：dragon, ninja, iceman, lion, wolf
        hp_list = list(map(int, input[ptr:ptr+5]))
        ptr += 5

        # 初始化红蓝司令部
        red_hq = Headquarter("red", M, hp_list)
        blue_hq = Headquarter("blue", M, hp_list)
        time = 0

        # 循环直到双方都停止制造
        while not red_hq.stopped or not blue_hq.stopped:
            events = []  # 存储当前时间的事件，先红后蓝

            # 1. 处理红方
            if not red_hq.stopped:
                success, name, wid, hp, remain = red_hq.try_make()
                if success:
                    # 生成降生事件
                    idx = NAME2IDX[name]
                    cnt = red_hq.cnt[idx]
                    line = f"{time:03d} red {name} {wid} born with strength {hp},{cnt} {name} in red headquarter"
                    events.append(("born", line, name, wid, remain, hp))
                else:
                    # 生成停止事件
                    line = f"{time:03d} red headquarter stops making warriors"
                    events.append(("stop", line))

            # 2. 处理蓝方
            if not blue_hq.stopped:
                success, name, wid, hp, remain = blue_hq.try_make()
                if success:
                    idx = NAME2IDX[name]
                    cnt = blue_hq.cnt[idx]
                    line = f"{time:03d} blue {name} {wid} born with strength {hp},{cnt} {name} in blue headquarter"
                    events.append(("born", line, name, wid, remain, hp))
                else:
                    line = f"{time:03d} blue headquarter stops making warriors"
                    events.append(("stop", line))

            # 3. 输出当前时间的所有事件
            for event in events:
                if event[0] == "stop":
                    print(event[1])
                else:
                    # 打印降生行 + 额外属性行
                    print(event[1])
                    print_warrior_extra(event[2], event[3], event[4], event[5])

            time += 1


if __name__ == "__main__":
    main()
