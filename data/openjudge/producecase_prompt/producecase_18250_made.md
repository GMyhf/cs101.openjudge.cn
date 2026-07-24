请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。题面的heights[r][c]缺少范围，也请给出。



## 18250:冰阔落 I

老王喜欢喝冰阔落。

初始时刻，桌面上有n杯阔落，编号为1到n。老王总想把其中一杯阔落倒到另一杯中，这样他一次性就能喝很多很多阔落，假设杯子的容量是足够大的。

有m 次操作，每次操作包含两个整数x与y。

若原始编号为x 的阔落与原始编号为y的阔落已经在同一杯，请输出"Yes"；否则，我们将原始编号为y 所在杯子的所有阔落，倒往原始编号为x 所在的杯子，并输出"No"。

最后，老王想知道哪些杯子有冰阔落。



输入

有多组测试数据，少于 5 组。
每组测试数据，第一行两个整数 n, m (n, m<=50000)。接下来 m 行，每行两个整数 x, y (1<=x, y<=n)。

输出

每组测试数据，前 m 行输出 "Yes" 或者 "No"。
第 m+1 行输出一个整数，表示有阔落的杯子数量。
第 m+2 行有若干个整数，从小到大输出这些杯子的编号。

样例输入

```
3 2
1 2
2 1
4 2
1 2
4 3
```

样例输出

```
No
Yes
2
1 3 
No
No
2
1 4
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
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

def union(x, y):
    root_x = find(x)
    root_y = find(y)
    if root_x != root_y:
        parent[root_y] = root_x

while True:
    try:
        n, m = map(int, input().split())
        parent = list(range(n + 1))

        for _ in range(m):
            a, b = map(int, input().split())
            if find(a) == find(b):
                print('Yes')
            else:
                print('No')
                union(a, b)

        unique_parents = set(find(x) for x in range(1, n + 1))  # 获取不同集合的根节点
        ans = sorted(unique_parents)  # 输出有冰阔落的杯子编号
        print(len(ans))
        print(*ans)

    except EOFError:
        break
```

