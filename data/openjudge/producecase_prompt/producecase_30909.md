请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 最优爬山路径

> 小P要从一块山地的一头走到另一头。山地可以看作是一个由n×m个单元构成的网格，每个单元有一个高度值。
> 小P要从左上角的单元走到右下角的单元。小P只能沿着东西南北四个方向走。小P有恐高症，又讨厌爬升，所以他想要找一条路，使得路上高度差的绝对值最大的相邻两个单元格的高度差的绝对值H尽可能小。问H最小可以是多少。
>
> **输入**
>
> 第1行是整数n和m,表示山地是一个n×m的网格( 1 < n,m <= 100)
> 接下来有n行，每行有m个整数，描述了山地中所有单元的高度h。 （0 <= h <= 10000)
>
> **输出**
>
> 最小的H
>
> 样例输入
>
> ```
> 3 3
> 1 3 8
> 2 1 5
> 4 6 3
> ```
>
> 样例输出
>
> ```
> 3
> ```





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


for epoch in range(30):
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
import sys
from collections import deque


def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    grid = []
    idx = 2
    for _ in range(n):
        grid.append([int(x) for x in input_data[idx : idx + m]])
        idx += m

    # BFS 函数：验证在最大高度差限制为 H 的情况下，能否从起点走到终点
    def can_reach(H):
        visited = [[False] * m for _ in range(n)]
        queue = deque([(0, 0)])
        visited[0][0] = True

        # 四个移动方向：上下左右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c = queue.popleft()

            # 成功到达终点
            if r == n - 1 and c == m - 1:
                return True

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    if not visited[nr][nc]:
                        # 检查高度差是否在限制 H 以内
                        if abs(grid[r][c] - grid[nr][nc]) <= H:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
        return False

    # 确定二分查找的上下边界
    flat_grid = [val for row in grid for val in row]
    min_val = min(flat_grid)
    max_val = max(flat_grid)

    low = 0
    high = max_val - min_val
    ans = high

    # 二分查找
    while low <= high:
        mid = (low + high) // 2
        if can_reach(mid):
            ans = mid
            high = mid - 1  # 尝试寻找更小的可行高度差
        else:
            low = mid + 1  # 限制太小，增加高度差

    print(ans)


if __name__ == "__main__":
    solve()
```

