请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 30887:Equal Sequence



输入

The first line contains a single integer n (1 <= n <= 10^5).
The second line contains n integers a1,a2,a3,...an (1 <= ai <= a^9).

输出

Print a single integer — the minimum number of operations.

样例输入

```
#1
3
1 2 3

#2
2
1 4

#3
5
1 2 3 4 5

#4
1
7
```

样例输出

```
#1
3

#2
2

#3
6

#4
0
```

提示

In the first example the optimal target is 1 (cost 0 + 1 + 2 =3) or 2 (cost 2 + 0 + 1 = 3), both requiring 3 operations.


In the second example set the target to 3: element 1 needs one +2 operation (1 -> 3) and element 4 needs one -1 operation (4 -> 3), for a total of 2 operations.


In the third example the optimal target is 3 with cost 1 + 2 + 0 + 1 + 2 = 6 .



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

def calc(a, target):
    """
    计算将数组 a 中所有元素变换到 target 的总代价
    """
    ans = 0
    for x in a:
        d = target - x
        if d <= 0:
            # 情况 1: x >= target
            # 数值需要变小，每减少 1 单位代价为 1
            ans += -d
        else:
            # 情况 2: x < target
            # 数值需要变大。根据题目逻辑：
            # 如果差值 d 是偶数，代价为 d / 2
            # 如果差值 d 是奇数，代价为 (d + 3) / 2
            if d % 2 == 0:
                ans += d // 2
            else:
                ans += (d + 3) // 2
    return ans

def main():
    # 使用 sys.stdin.read().split() 快速读取大规模数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:n+1]))
    
    # 第一步：排序。为了通过中位数性质找到最优解
    a.sort()
    
    # 第二步：确定目标值 q
    # 在代价不对等的情况下，最优解会向代价高的方向偏移
    # 这里的 k 经过数学推导约为 (2n)/3 的位置
    k = (2 * n + 2) // 3 
    
    # 取排序后第 k 个数作为基准
    q = a[k - 1]
    
    # 第三步：计算 q 和 q-1 两种情况下的代价，取最小值
    # 因为代价函数在 q 附近可能有波动，检查相邻点更稳妥
    res = min(calc(a, q - 1), calc(a, q))
    
    print(res)

if __name__ == "__main__":
    main()
```

