下面是现有的一个编程题目，以及它的ac.py。想变形为一个“边的权值不均为 1”的新题目，给出标题，题面（包括描述、输入、输出、样例和提示），相应ac的代码，以及请根据生成数据的模版 producecase_template.py，给出新变形题目的生产数据的 producecase.py



## 01最小生成树

总时间限制: 10000ms 单个测试点时间限制: 1000ms内存限制: 131072kB

给定一张 n 个点的完全图. 图中所有边的边权均为 0/1, 且有且仅有 m 条边边权为 1.

求解该完全图的最小生成树, 你只需要输出最小生成树的边权和即可.

**输入**

第一行两个数字 n, m 表示点数,以及边权为 1 的边数。(m <= min{200000, n(n-1)/2})

接下来 m 行, 一行两个数字 a[i],b[i], 表示连接 a[i],b[i] 的边,其边权为 1(1 <= a[i] < b[i] <= n). 保证输入的边两两不同.

**输出**

一行一个数字,表示最小生成树的边权和.

样例输入

```
6 11
1 3
1 4
1 5
1 6
2 3
2 4
2 5
2 6
3 4
3 5
3 6
===========
3 0
```

样例输出

```
2
===========
0
```

提示

Subtask1 (20%): n <= 300。

Subtask2 (80%): n <= 100000。





ac.py

```python
from collections import deque

n, m = map(int, input().split())

# 特殊情况：n == 1
if n == 1:
    print(0)
    exit()

graph1 = [set() for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph1[a].add(b)
    graph1[b].add(a)

unvisited = set(range(1, n + 1))
components = 0

while unvisited:
    start = unvisited.pop()
    components += 1
    queue = deque([start])

    while queue:
        u = queue.popleft()
        # 找出所有未访问且 (u,v) 不是1-边 的点 → 即0-边可达
        # bad = graph1[u] ∩ unvisited
        # good = unvisited - bad
        bad = graph1[u]
        if not bad:
            continue

        # 注意：bad 是 set，unvisited 是 set，可以直接减
        good = unvisited - bad
        for v in good:
            queue.append(v)
        unvisited -= good

print(components - 1)
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

