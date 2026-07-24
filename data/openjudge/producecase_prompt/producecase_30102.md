请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。题面的heights[r][c]缺少范围，也请给出。



## T30102:完美交易窗口

总时间限制: 1000ms 内存限制: 131072kB

作为一名量化交易员，你正在分析一只股票连续 N 秒内的价格数据，记录为一个数组 `h = [h1, h2, ..., hN]`。

根据你的三十年量化经验，你定义了一种“完美交易窗口”，并且想找出这组数据中最长的完美交易窗口有多少秒。具体地，“完美交易窗口” 是一个从第 `i` 秒到第 `j` 秒的连续时间段 `[i...j]`，且必须满足以下所有条件：

1. **完美买入:** 必须在第 `i` 秒买入，且 `h[i]` 必须是 `[i...j]` 这整个时间窗口内的**最低**价格。
2. **完美卖出：**必须在第 `j` 秒卖出，且 `h[j]` 必须是 `[i...j]` 这整个时间窗口内的**最高**价格。
3. **盈利交易：**卖出价 `h[j]` 必须**严格大于**买入价 `h[i]` (即 `h[j] > h[i]`)。
4. **严格完美：**在持有期间（即第 `k` 秒，`i < k < j`），股价既不能等于你的买入价 `h[i]`，也不能等于你的卖出价 `h[j]`。

输入

第一行包含一个整数 N (2 <= N <= 1,000,000)，代表数据的持续时间（以秒为单位）。
接下来 N 行，每行包含一个整数 hi (1 <= hi < 2^31)，代表第 i 秒的股票价格。

输出

一行，包含一个整数，表示最长的“完美交易窗口”有多少秒。

样例输入

```
10
3
1
2
5
4
6
1
2
4
3
```

样例输出

```
5
```

提示

tag: monotonic stack, binary search



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
from bisect import bisect_right
from array import array

def solve():
    # 1. 读入数据 (尽量用内存友好的方式)
    raw = sys.stdin.read().split()
    if not raw: return
    n = int(raw[0])
    h = array('I', map(int, raw[1:]))

    # max_stk: 找左侧第一个 >= h[j] 的位置 (单调递减栈)
    max_stk = []
    # buy_stk: 存潜在的买入点 i (单调递增栈)
    buy_stk = []
    
    ans = 0

    # 遍历每一秒，把它作为“卖出点”
    for j in range(n):
        cur_p = h[j]

        # --- 步骤 A: 确定 h[j] 作为最高价的左边界 ---
        # 只要左边比我小，它就挡不住我，踢走
        while max_stk and h[max_stk[-1]] < cur_p:
            max_stk.pop()
        # 此时栈顶就是左边第一个 >= 我的位置
        left_barrier = max_stk[-1] if max_stk else -1

        # --- 步骤 B: 更新买入候选人 ---
        # 如果我比之前的买入点还便宜，那之前的买入点就不是唯一最小值了，踢走
        while buy_stk and h[buy_stk[-1]] >= cur_p:
            buy_stk.pop()

        # --- 步骤 C: 在候选人里挑一个最好的 ---
        # 我们需要在 buy_stk 里找第一个 > left_barrier 的下标
        if buy_stk:
            # 二分查找：找到 buy_stk 中第一个大于 left_barrier 的位置
            idx = bisect_right(buy_stk, left_barrier)
            
            if idx < len(buy_stk):
                # 找到了！这个 best_i 就是能构成的最长窗口的左端点
                best_i = buy_stk[idx]
                ans = max(ans, j - best_i + 1)

        # 把自己存进去，既可能是未来的左边界，也可能是未来的买入点
        max_stk.append(j)
        buy_stk.append(j)

    print(ans)

solve()

```

