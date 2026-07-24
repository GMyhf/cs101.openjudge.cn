请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py



## 复制粘贴

Alice 有两个字符串 S 和 T，她的希望通过对字符串 T 进行一系列操作，使得字符串 S 为字符串T的一个子序列。这里的“子序列”是指通过从一个字符串中删除一些字符（可以是零个或多个，也可以不删），但不改变剩余字符的顺序，得到的新字符串。

Alice 可以进行的操作有两种：复制和粘贴。其中复制操作会将目前整个T串覆写到剪切板，粘贴操作会将剪切板的内容新增在T串的末尾。注意，一开始剪切板为空，并且粘贴操作不会清空剪切板。

现在，你需要回答，Alice 至少需要操作多少次才能达到目的？如果无论怎样操作，Alice 都无法达到目的，请你输出 “-1”（不包含引号）。

输入

第一行输入一个只包含小写字母的字符串 S(1≤|S|≤10^5)；
第二行输入一个只包含小写字母的字符串 T(1≤|T|≤10^5)。

输出

输出一个整数，表示 Alice 需要操作的次数。

样例输入

```
abbbbbbbbb
cbaca
```

样例输出

```
7
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
import sys
from bisect import bisect_left

def solve():
    # 使用 sys.stdin.read 一次性读取，防止多次 I/O 带来的开销
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    s = input_data[0]
    t = input_data[1]
    
    n = len(s)
    m = len(t)
    
    # 1. 预处理 T 中每个字符出现的所有索引位置
    char_indices = [[] for _ in range(26)]
    ord_a = ord('a')
    for i, char in enumerate(t):
        char_indices[ord(char) - ord_a].append(i)
        
    # 2. 贪心计算最少需要的副本数 k
    k = 1
    curr_pos = 0 # 当前在 T 副本中的匹配位置
    
    for char in s:
        indices = char_indices[ord(char) - ord_a]
        if not indices:
            # S 中存在 T 中没有的字符，无法匹配
            print("-1")
            return
            
        # 使用二分查找寻找当前副本中第一个大于等于 curr_pos 的字符索引
        it = bisect_left(indices, curr_pos)
        
        if it < len(indices):
            # 在当前副本的剩余部分找到了
            curr_pos = indices[it] + 1
        else:
            # 当前副本匹配完了，需要开启一个新副本
            k += 1
            curr_pos = indices[0] + 1
            
    # 如果 1 个副本就够了，不需要任何操作
    if k == 1:
        print(0)
        return
        
    # 3. DP 计算最少操作次数
    # 这是一个经典的“复制与粘贴”问题，目标是得到至少 k 个副本。
    # 达到 x 个副本的最少次数等于其所有质因数之和。
    # 由于可以超过 k，我们需要在一个范围内寻找最小值。
    
    # 设置上限。考虑到 2^17 > 10^5，在这个范围内一定能找到最优解。
    limit = max(k + 500, 131072) 
    if limit > 200005: 
        limit = 200005
        
    # dp[i] 表示得到恰好 i 个副本的最少操作次数
    # 初始值设为 i，表示 1 次复制后进行 i-1 次粘贴
    dp = list(range(limit + 1))
    dp[0] = 0
    dp[1] = 0
    
    # 状态转移：从 i 个副本出发，复制一次，粘贴 (j-1) 次，得到 i*j 个副本
    # 总代价 = dp[i] + j
    for i in range(2, limit // 2 + 1):
        base_cost = dp[i]
        # v = i * j, 则 j = v // i
        # 这个循环类似于素数筛法，复杂度为 O(N log N)
        for v in range(i * 2, limit + 1, i):
            cost = base_cost + (v // i)
            if cost < dp[v]:
                dp[v] = cost
                
    # 在所有大于等于 k 的副本数中找最小值
    print(min(dp[k:]))

if __name__ == "__main__":
    solve()
```

