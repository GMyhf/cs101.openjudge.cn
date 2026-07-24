请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 邮递员送快递

> 某县有n个村庄，由一个邮递员负责送快递。村庄编号1到n。邮局在村庄 1。他总共要送 n-1 样东西，其目的地分别是村庄 2 到村庄 n。
> 由于这个县地方小且交通比较繁忙，因此所有的道路都是单行的，共有 m 条道路，每条道路直接连接两个村庄。这个邮递员每次只能带一样东西，并且运送每件物品过后必须返回邮局。求送完这 n-1 样东西并且最终回到邮局最少需要的时间。
>
> **输入**
>
> 第一行包括两个整数，n 和 m，表示村庄的村庄数量和道路数量。(n 不超过 1100,m 不超过 100000）
>
> 接下来的m行，每行三个整数，u,v,w，表示从村庄 u 到村庄 v 有一条通过时间为 w 的道路
>
> **输出**
>
> 输出仅一行，包含一个整数，为最少需要的时间。
>
> 样例输入
>
> ```
> 5 10
> 2 3 5
> 1 5 5
> 3 5 6
> 1 2 8
> 1 3 8
> 5 3 4
> 4 1 8
> 4 5 3
> 3 5 6
> 5 4 2
> ```
>
> 样例输出
>
> ```
> 83
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
import heapq

def solve():
    data = list(map(int, sys.stdin.read().split()))
    it = iter(data)
    n = next(it); m = next(it)
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = next(it); v = next(it); w = next(it)
        g[u].append((v, w))
        rg[v].append((u, w))

    def dijkstra(graph, start):
        dist = [float('inf')] * (n + 1)
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
        return dist

    d1 = dijkstra(g, 1)
    d2 = dijkstra(rg, 1)
    ans = sum(d1[i] + d2[i] for i in range(2, n + 1))
    print(ans)

if __name__ == "__main__":
    import sys
    solve()
```

