请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py





小明穿越到了一个扭曲空间，在这个空间中进行移动所消耗的移动成本与方向有关。

在这个空间建立一个笛卡尔坐标系，小明的位置为为原点。

他每一次可以移动到相邻的 8 个格点处，沿x轴、沿y轴以及沿对角线方向的移动成本分别为a，b，c

比如从 (0,0) 移动到 (1,0) 的成本为 a，从 (0,0) 移动到 (0,1) 的成本为 b，从 (0,0) 移动到 (1,1) 的成本为c

小明为了穿越回去，需要收集散落在空间中的 3 个零件，并最终到达位于 (100,100) 处的装置才行，请你帮小明规划一条最短的移动路线，让他尽快可以穿越回去。

**输入**
输入为4行
第一行是a b c，以空格分隔，均为非负实数
接下来为3行，每行为 s x y，以空格分隔，表示零件的名称s以及x和y坐标，s由不超过20个非空字符组成，x，y均为整数且-100 < x,y < 100

**输出**
输出为两行
第一行为拾取零件的顺序，将所有零件按顺序输出它们的名称，以空格分隔

第二行为小明从原点移动到装置的最短路径，并保留两位小数

例子输入

```
1.0 1.0 1.4
Adamantium 92 40
infinity_gauntlet -74 -25
decade_armor 95 72
```

例子输出

```
infinity_gauntlet Adamantium decade_armor
339.20
```



```python
import sys
from itertools import permutations


# 用数学计算替代 Dijkstra 搜索
def get_cost(p1, p2, a, b, c):
    # 1. 预处理成本（处理三角不等式）
    # 确保直走不会比斜着走还贵，斜着走不会比直走两步还贵
    # 实际上只需要确保 c <= a + b 且 a <= b + c 等
    # 为防万一，循环更新一下最小值
    for _ in range(3):
        a = min(a, b + c)
        b = min(b, a + c)
        c = min(c, a + b)

    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])

    # 核心公式：
    # 尽可能多走对角线 (min(dx, dy) 步)
    # 剩下的走直线 (abs(dx - dy) 步)
    min_delta = min(dx, dy)
    rem_delta = abs(dx - dy)

    cost = min_delta * c
    if dx > dy:
        cost += rem_delta * a
    else:
        cost += rem_delta * b

    return cost


def solve():
    # 输入处理
    # 建议使用 sys.stdin 读取，防止某些环境 input() 报错或慢
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        a = float(next(iterator))
        b = float(next(iterator))
        c = float(next(iterator))

        parts = []
        for _ in range(3):
            name = next(iterator)
            x = int(next(iterator))
            y = int(next(iterator))
            parts.append((name, x, y))
    except StopIteration:
        return

    # 起点和终点
    start_node = (0, 0)
    end_node = (100, 100)

    # 构建所有关键点的列表：Start(0), Part1(1), Part2(2), Part3(3), End(4)
    points = [start_node] + [(p[1], p[2]) for p in parts] + [end_node]

    # 预计算距离矩阵 (5x5)
    n = len(points)
    dist_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = get_cost(points[i], points[j], a, b, c)
            dist_matrix[i][j] = d
            dist_matrix[j][i] = d

    # 枚举全排列 (中间3个零件的顺序)
    # 零件在 points 列表中的索引是 1, 2, 3
    min_total_cost = float('inf')
    best_order_indices = []

    for p in permutations([1, 2, 3]):
        # 路径: Start(0) -> p[0] -> p[1] -> p[2] -> End(4)
        current_cost = 0
        current_path = [0] + list(p) + [4]

        for i in range(len(current_path) - 1):
            u = current_path[i]
            v = current_path[i + 1]
            current_cost += dist_matrix[u][v]

        if current_cost < min_total_cost:
            min_total_cost = current_cost
            best_order_indices = list(p)

    # 输出结果
    # 零件名称顺序
    res_names = [parts[i - 1][0] for i in best_order_indices]
    print(" ".join(res_names))
    print(f"{min_total_cost:.2f}")


if __name__ == "__main__":
    solve()
```



producecase_template.py

```python
import random
import time
import os

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve(m, n, k):
    """等价类划分问题逻辑 (ac.py 同款)"""
    groups = {}
    for num in range(m + 1, n):
        s = sum(map(int, str(num)))
        if s % k == 0:
            groups.setdefault(s, []).append(num)

    result_lines = []
    for s in sorted(groups):
        result_lines.append(','.join(map(str, sorted(groups[s]))))
    return result_lines


for epoch in range(20):
    # 随机生成 m, n, k
    m = random.randint(1, 9000)
    n = random.randint(m + 2, min(m + 2000, 10000))  # 保证范围合理
    k = random.randint(1, 9)

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(f"{m},{n},{k}\n")

    start = time.time()

    # 调用逻辑
    result = solve(m, n, k)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | m={m}, n={n}, k={k}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        if result:
            f.write("\n".join(result) + "\n")
        else:
            f.write("\n")  # 没有满足条件的情况


```



ac.py

```python
def solve():
    """
    计算 k 根柱子移动 n 个圆盘所需的最少步骤数
    """
    import sys
    
    # 从标准输入读取数据
    # 输入格式为一行：k n
    try:
        input_line = sys.stdin.readline().split()
        if not input_line:
            return
        k = int(input_line[0])
        n = int(input_line[1])
    except ValueError:
        return

    # dp[i][j] 表示：有 j 根柱子时，移动 i 个圆盘所需的最少步骤数
    # 初始化数组，大小为 (n+1) x (k+1)，初始值为无穷大
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]

    # === 初始化边界条件 ===

    # 1. 0 个圆盘需要 0 步
    for j in range(3, k + 1):
        dp[0][j] = 0

    # 2. 3 根柱子的情况（经典汉诺塔）
    # 公式为：2^i - 1
    for i in range(1, n + 1):
        dp[i][3] = 2**i - 1
        
    # 3. 任何柱子数量下，移动 1 个圆盘只需要 1 步
    for j in range(3, k + 1):
        dp[1][j] = 1

    # === 动态规划计算 ===
    
    # 外层循环：柱子数量 j 从 4 增加到 k
    for j in range(4, k + 1):
        # 内层循环：圆盘数量 i 从 2 增加到 n
        for i in range(2, n + 1):
            min_steps = float('inf')
            
            # 核心状态转移：
            # 尝试将 i 个盘子分割为两部分：
            # 上面 x 个盘子（使用 j 根柱子移动到缓冲区）
            # 下面 i-x 个盘子（使用 j-1 根柱子移动到目标区，因为有一根柱子被 x 占用了）
            # 最后再把 x 个盘子移回目标区（使用 j 根柱子）
            # 总步数 = 2 * dp[x][j] + dp[i-x][j-1]
            
            for x in range(1, i):
                current_steps = 2 * dp[x][j] + dp[i - x][j - 1]
                if current_steps < min_steps:
                    min_steps = current_steps
            
            dp[i][j] = min_steps

    # 输出结果
    print(dp[n][k])

if __name__ == "__main__":
    solve()
```

