请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py



## 两座孤岛最短距离

给一个由1跟0组成的方形地图，1代表土地，0代表水域

相邻(上下左右4个方位当作相邻)的1组成孤岛

现在你可以将0转成1，搭建出一个链接2个孤岛的桥

请问最少要将几个0转成1，才能建成链接孤岛的桥。

题目中恰好有2个孤岛(顾答案不会是0)



输入

一个正整数n，代表几行输入
n行0跟1字串

输出

一个正整数k，代表最短距离

样例输入

```
3
110
000
001
```

样例输出

```
2
```

提示

样例输入中的两个孤岛最短距离为2



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
import sys
from collections import deque

sys.setrecursionlimit(10**9)

move = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def tong(x, y, q, maze):
    """DFS标记第一个岛屿，并将边界点加入队列"""
    maze[x][y] = '2'
    q.append((x, y))
    for dx, dy in move:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and maze[nx][ny] == '1':
            tong(nx, ny, q, maze)

def bfs(q, maze):
    """BFS寻找第二个岛屿的最短距离"""
    s = 0
    while q:
        for _ in range(len(q)):
            x, y = q.popleft()
            for dx, dy in move:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if maze[nx][ny] == '1':  # 找到第二个岛屿
                        return s
                    if maze[nx][ny] == '0':  # 水域，加入队列
                        maze[nx][ny] = '2'  # 标记为访问过
                        q.append((nx, ny))
        s += 1
    return s

# 主函数
n = int(input())
maze = [list(input()) for _ in range(n)]
q = deque()
found = False  # 标记是否找到第一个岛屿

for i in range(n):
    if found:
        break
    for j in range(n):
        if maze[i][j] == '1':  # 找到第一个岛屿
            tong(i, j, q, maze)
            print(bfs(q, maze))
            found = True
            break
```

