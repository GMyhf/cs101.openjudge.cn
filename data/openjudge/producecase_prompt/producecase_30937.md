请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 01最小生成树

> 
>
> 输入
>
> 第一行两个数字 n, m 表示点数,以及边权为 1 的边数。(m <= min{200000, n(n-1)/2})
>
> 接下来 m 行, 一行两个数字 a[i],b[i], 表示连接 a[i],b[i] 的边,其边权为 1(1 <= a[i] < b[i] <= n). 保证输入的边两两不同.
>
> 输出
>
> 一行一个数字,表示最小生成树的边权和.
>
> 样例输入
>
> ```
> sample1 input:
> 6 11
> 1 3
> 1 4
> 1 5
> 1 6
> 2 3
> 2 4
> 2 5
> 2 6
> 3 4
> 3 5
> 3 6
> 
> sample1 output:
> 2
> ```
>
> 样例输出
>
> ```
> sample2 input:
> 3 0
> 
> sample2 output:
> 0
> 
> sample3 input:
> 6 10
> 1 3
> 1 4
> 1 5
> 1 6
> 2 3
> 2 4
> 2 6
> 3 5
> 3 6
> 4 5
> 
> sample3 output:
> 0
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
from collections import deque

n, m = map(int, input().split())
graph1 = [set() for _ in range(n+1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph1[a].add(b)
    graph1[b].add(a)

unvisited = set(range(1, n+1))
components = 0

while unvisited:
    start = unvisited.pop()
    components += 1
    queue = deque([start])
    while queue:
        u = queue.popleft()
        good = unvisited - graph1[u]  # 所有未访问且与 u 有 0-边的点
        for v in good:
            queue.append(v)
        unvisited -= good

print(components - 1)
```

