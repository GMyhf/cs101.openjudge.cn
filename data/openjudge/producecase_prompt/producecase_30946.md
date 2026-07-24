请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 智能传送带的路径数



> 在自动化智能仓库中，有一条长度为 $N$ 的传送带，被划分为 $0$ 到 $N-1$ 的网格。某些网格上可能有障碍物，其余网格是空闲的。
> 一个智能机器人需要将货物从起点 $0$ 传送到终点 $N-1$。货物在传送带上的每一次移动都有距离限制，且不能落在有障碍物的网格上。为了评估系统的冗余度，工程师需要知道：**一共有多少种不同的传送方案**能将货物成功送达终点？
>
> 给你一个下标从 `0` 开始、长度为 `N` 的二进制字符串 `S`，其中 `'0'` 表示空闲网格，`'1'` 表示有障碍物的网格。同时给你两个整数 `L` 和 `R`，表示单次移动的最小距离和最大距离。
>
> 一开始，货物位于下标 `0` 处（保证 `S[0] == '0'`）。当同时满足如下条件时，货物可以从下标 `i` 传送到下标 `j` 处：
>
> - `i + L <= j <= min(i + R, N - 1)` 且
> - `S[j] == '0'`.
>
> 请计算从起点 `0` 到达终点 `N-1` 的**不同传送方案总数**。由于方案数可能非常大，请将结果对 $10^9 + 7$ 取模后输出。
>
> 数据范围
>
> - 2 <= N <= 10^5
>
> - 1 <= L <= R < N
>
> - $S[i]$ 要么是 `'0'`，要么是 `'1'`
>
> - $S[0] == '0'$
>
>   
>
> **输入**
>
> 输入包含两行：
>
> - 第一行包含三个整数 $N, L, R$ （以空格分隔），分别表示传送带的长度、单次传送的最小距离和最大距离。
> - 第二行包含一个长度为 $N$ 的二进制字符串 $S$。
>
> **输出**
>
> 输出一个整数，表示到达网格 $N-1$ 的不同方案数对 $10^9 + 7$ 取模后的结果。如果无法到达终点，则输出 `0`。
>
> 样例输入 
>
> ```text
> sample1 input:
> 6 2 3
> 011010
> 
> sample1 output:
> 1
> 
> # 起点为 0。
> - 第一步：只能从 0 移动到 3（移动距离为 3，且 S[3] == '0'）。
> - 第二步：只能从 3 移动到 5（移动距离为 2，且 S[5] == '0'）。
>   只有 0 -> 3 -> 5 这一条路径，因此方案数为 1。
> ```
>
> 样例输出
>
> ```text
> sample2 input:
> 8 2 3
> 00000000
> 
> sample2 output:
> 3
> 
> # 共有 3 种不同的传送方案：0 -> 2 -> 4 -> 7
> 0 -> 2 -> 5 -> 7, 0 -> 3 -> 5 -> 7
> ```
>
> 提示：动态规划 + 滑动窗口

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

def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    l = int(input_data[1])
    r = int(input_data[2])
    s = input_data[3]
    
    MOD = 1000000007
    
    # 如果终点有障碍物，直接返回 0
    if s[n - 1] == '1':
        print(0)
        return
    
    # dp[i] 表示到达位置 i 的方案数
    dp = [0] * n
    dp[0] = 1 # 起点初始化为 1 种方案
    
    window_sum = 0
    
    for i in range(1, n):
        # 1. 元素进入窗口：i - l 进入有效前驱区间
        if i >= l:
            window_sum = (window_sum + dp[i - l]) % MOD
            
        # 2. 元素离开窗口：i - r - 1 移出有效前驱区间
        if i > r:
            window_sum = (window_sum - dp[i - r - 1] + MOD) % MOD
            
        # 3. 计算当前位置的 dp 值
        if s[i] == '0':
            dp[i] = window_sum
        else:
            dp[i] = 0
            
    print(dp[n - 1])

if __name__ == '__main__':
    solve()
```

