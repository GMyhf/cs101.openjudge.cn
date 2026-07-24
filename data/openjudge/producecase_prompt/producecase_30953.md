请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 魔法森林

http://dsaex.openjudge.cn/2026mockexam/E/

在古老的幻境国度，有一片传说中的幽秘森林。这片森林里生长着无数的魔法树，每一棵树上都栖息着爱搞恶作剧的精灵。整片森林被神秘的单向魔法路径缠绕，形成了一张扑朔迷离的网络。这些路径只能单向通行，无法逆行。

传说中，森林里的魔法树共有 N 棵，它们被奇异的编号标记，从 1 到 N。森林中存在 M 条单向魔法路径，每条路径将两棵树连接起来。

某天，森林里的精灵们突发奇想，决定玩一个令人费解的游戏：每个精灵都要找到从自己栖息的魔法树出发，沿着单向的魔法路径，最终能够到达的编号最小的魔法树。传说在这棵编号最小的魔法树上，隐藏着一个无尽智慧的宝藏。

精灵们的聪明才智似乎到达了极限，于是它们向外界发布了一个挑战，希望有智慧的冒险者们能够解开这个谜题。你，作为一个足智多谋的冒险者，决定接受这个挑战。

你的任务是：对于每一棵魔法树 v，找出从它出发，沿着单向的魔法路径，能够到达的编号最小的魔法树。你需要编写一个程序来实现这一点，并帮助精灵们找到它们的梦想之树。



输入

第一行包含两个整数 N 和 M，分别表示魔法树的数量和魔法路径的数量。

接下来的 M 行，每行包含两个整数 u 和 v，表示存在一条从魔法树 u 到魔法树 v 的单向魔法路径。

输出

用空格隔开的 N 个数，第 i 个数表示从第 i 棵魔法树出发，能够到达的编号最小的魔法树。

样例输入

```
5 4
1 3
3 4
4 5
4 2
```

样例输出

```
1 2 2 2 5
```

提示

1 ≤ N, M ≤ 10^5



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
    # 快速读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    
    # 建立反向邻接表
    # adj[v] 存储所有指向 v 的节点 u (即原图中的 u -> v，反向图中的 v -> u)
    adj = [[] for _ in range(N + 1)]
    
    idx = 2
    for _ in range(M):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        idx += 2
        adj[v].append(u)
        
    # ans[i] 表示从节点 i 出发能到达的最小节点编号
    ans = [0] * (N + 1)
    
    # 从 1 到 N 依次作为终点（反向图的起点）进行 BFS
    for i in range(1, N + 1):
        if ans[i] != 0:
            continue
        
        # 初始化队列开始 BFS
        queue = deque([i])
        ans[i] = i
        
        while queue:
            curr = queue.popleft()
            for neighbor in adj[curr]:
                if ans[neighbor] == 0:
                    ans[neighbor] = i
                    queue.append(neighbor)
                    
    # 输出结果，节点编号从 1 到 N
    print(*(ans[1:]))

if __name__ == '__main__':
    solve()
```

