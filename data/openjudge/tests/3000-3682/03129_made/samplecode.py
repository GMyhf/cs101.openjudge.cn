# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 3129: 魔兽世界之一：备战
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/03129/
# License: not declared; no license is inferred.
import sys

# 武士制造顺序常量
RED_ORDER = ['iceman', 'lion', 'wolf', 'ninja', 'dragon']
BLUE_ORDER = ['lion', 'dragon', 'ninja', 'iceman', 'wolf']

class Headquarter:
    def __init__(self, color, m, costs, order):
        self.color = color         # 阵营颜色
        self.m = m                 # 当前生命元
        self.costs = costs         # 每种武士的消耗字典
        self.order = order         # 该阵营的制造顺序列表
        self.cur_idx = 0           # 当前应该尝试制造的武士在列表中的索引
        self.total_count = 0       # 总武士编号（从1开始）
        self.type_counts = {name: 0 for name in costs} # 每种武士的数量统计
        self.stopped = False       # 是否已经停止制造

    def produce(self, time):
        """尝试在给定时间制造一个武士"""
        if self.stopped:
            return

        # 尝试制造当前顺序下的武士，如果不行就试下一个，最多试5种
        for _ in range(5):
            name = self.order[self.cur_idx]
            cost = self.costs[name]

            if self.m >= cost:
                # 能够制造
                self.m -= cost
                self.total_count += 1
                self.type_counts[name] += 1

                # 输出格式：000 red iceman 1 born with strength 5,1 iceman in red headquarter
                print(f"{time:03d} {self.color} {name} {self.total_count} born with strength {cost},"
                      f"{self.type_counts[name]} {name} in {self.color} headquarter")

                # 指针移向下一个，下次从下一个开始尝试
                self.cur_idx = (self.cur_idx + 1) % 5
                return
            else:
                # 生命元不足，尝试下一个种类
                self.cur_idx = (self.cur_idx + 1) % 5

        # 如果循环了5次都无法制造，则停止
        self.stopped = True
        print(f"{time:03d} {self.color} headquarter stops making warriors")

def solve():
    # 使用 sys.stdin.read().split() 处理所有输入，提高读取效率并自动处理空格/换行
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    it = iter(input_data)
    num_cases = int(next(it))

    for i in range(1, num_cases + 1):
        m = int(next(it))
        # 输入顺序为：dragon, ninja, iceman, lion, wolf
        raw_costs = [int(next(it)) for _ in range(5)]
        names = ['dragon', 'ninja', 'iceman', 'lion', 'wolf']
        costs = dict(zip(names, raw_costs))

        # 初始化红蓝司令部
        red = Headquarter('red', m, costs, RED_ORDER)
        blue = Headquarter('blue', m, costs, BLUE_ORDER)

        print(f"Case:{i}")

        time = 0
        # 只要有一方还没停止，模拟就继续
        while not (red.stopped and blue.stopped):
            red.produce(time)
            blue.produce(time)
            time += 1

if __name__ == "__main__":
    solve()
