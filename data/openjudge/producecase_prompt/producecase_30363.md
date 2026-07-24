请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py

## 动态图连通性

有一个 n 个点的无向图，初始没有边。现在执行 q 次加边操作：每次操作给出两个点 u, v 并在图中加入无向边 (u, v)。你需要在每次操作后输出图中有多少对 x, y 满足 1 <= x <= y <= n，且 连通（即图中存在 x 到 y 的路径）.

**输入**

第一行两个正整数 n, q.
接下来 q 行每行两个正整数 u, v, 表示加入的边, 保证 1 <=u <=v <=n.

**输出**

q行, 每行一个整数, 第 i 行的表示第 i 次加边后的答案.

样例输入

```
5 5
4 1
5 2
4 5
5 4
4 3
```

样例输出

```
1
2
6
6
10
```

提示

并查集dsu
对所有数据 n <= 2 * 10^5, q <= 2 * 10^5.
对 30% 的数据: n <= 100.
对 60% 的数据: n <= 1000.





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
sys.setrecursionlimit(1 << 25)

def main():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    n = int(data[idx])
    idx += 1
    m = int(data[idx])
    idx += 1
    
    # 并查集初始化
    parent = list(range(n + 1))  # 点编号从1到n
    size = [1] * (n + 1)        # 每个连通分量的大小
    res = 0                     # 总答案
    
    def find(u):
        """查找根节点，带路径压缩"""
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]
    
    output = []
    for _ in range(m):
        u = int(data[idx])
        idx += 1
        v = int(data[idx])
        idx += 1
        
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # 减去两个分量原来的点对数
            res -= size[root_u] * (size[root_u] - 1) // 2
            res -= size[root_v] * (size[root_v] - 1) // 2
            # 合并分量
            if size[root_u] < size[root_v]:
                root_u, root_v = root_v, root_u
            parent[root_v] = root_u
            size[root_u] += size[root_v]
            # 加上合并后新分量的点对数
            res += size[root_u] * (size[root_u] - 1) // 2
        # 记录当前答案
        output.append(str(res))
    
    print('\n'.join(output))

if __name__ == "__main__":
    main()
```

