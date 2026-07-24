请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py





“骑士游历”问题是一道经典的问题：从1000*1000棋盘上的一点 (x1, y1) 出发，到另一点 (x2, y2) 的最短距离是多少？当然，骑士只能按照“日”字形走法来前进。
如何快速地得到这个问题的解？我们需要你在1秒的时间内算出这样的问题。

**输入**

第一行是测试数据的数目t（1 <= t <= 20）。

以下每行均包含四个整数x1 y1 x2 和y2，以空格分开，前两个是起点坐标，后两个是终点坐标。

0 <= x1, y1, x2, y2 <= 999。

**输出**

对应输入的每组数据，输出相应的最短距离。

样例输入

```
4
0 0 999 999
0 0 1 2
0 0 2 2
500 500 505 505
```

样例输出

```
666
1
4
4
```

提示

双向 BFS (Bi-directional BFS)



ac.py

```python
import sys
from collections import deque

# 棋盘大小
BOARD_SIZE = 1000

# 骑士的8个移动方向偏移量
MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1)
]


def bidirectional_bfs(start, end):
    """
    双向 BFS 计算最短路径
    start, end: 元组 (x, y)
    """
    if start == end:
        return 0

    # 初始化两个方向的队列
    # q_f: Forward queue (从起点开始)
    # q_b: Backward queue (从终点开始)
    q_f = deque([start])
    q_b = deque([end])

    # 记录访问过的节点及步数
    # dist_f: 从起点出发到达某点的步数
    # dist_b: 从终点出发到达某点的步数
    dist_f = {start: 0}
    dist_b = {end: 0}

    while q_f and q_b:
        # 核心优化：总是扩展节点数较少的那个队列
        # 这能保证搜索范围像两个均匀扩大的圆，效率最高
        if len(q_f) > len(q_b):
            q_f, q_b = q_b, q_f
            dist_f, dist_b = dist_b, dist_f

        # 取出当前队列的头节点
        curr_pos = q_f.popleft()
        curr_steps = dist_f[curr_pos]
        cx, cy = curr_pos

        # 尝试8个方向
        for dx, dy in MOVES:
            nx, ny = cx + dx, cy + dy

            # 边界检查 (0-999)
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                next_pos = (nx, ny)

                # 【相遇检测】：如果新节点已经在对方的访问记录里
                if next_pos in dist_b:
                    # 总步数 = 当前这边的步数 + 1 (跨出这一步) + 对方那边的步数
                    return curr_steps + 1 + dist_b[next_pos]

                # 如果当前方向没访问过，加入队列
                if next_pos not in dist_f:
                    dist_f[next_pos] = curr_steps + 1
                    q_f.append(next_pos)

    return -1


def main():
    # 使用 sys.stdin.read 一次性读取所有输入，处理速度最快
    input_data = sys.stdin.read().split()

    if not input_data:
        return

    iterator = iter(input_data)

    try:
        # 读取测试用例数量 t
        t = int(next(iterator))

        results = []
        for _ in range(t):
            # 依次读取 x1, y1, x2, y2
            x1 = int(next(iterator))
            y1 = int(next(iterator))
            x2 = int(next(iterator))
            y2 = int(next(iterator))

            start_pos = (x1, y1)
            end_pos = (x2, y2)

            # 计算并存储结果
            ans = bidirectional_bfs(start_pos, end_pos)
            results.append(str(ans))

        # 一次性输出所有结果
        print('\n'.join(results))

    except StopIteration:
        pass


if __name__ == "__main__":
    main()
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

