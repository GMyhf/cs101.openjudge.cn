请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。题面的heights[r][c]缺少范围，也请给出。



## 30571:十进制整数的反码

每个非负整数 `N` 都有其二进制表示。例如， `5` 可以被表示为二进制 `"101"`，`11` 可以用二进制 `"1011"` 表示，依此类推。注意，除 `N = 0` 外，任何二进制表示中都不含前导零。

二进制的反码表示是将每个 `1` 改为 `0` 且每个 `0` 变为 `1`。例如，二进制数 `"101"` 的二进制反码为 `"010"`。

给你一个十进制数 `N`，请你返回其二进制表示的反码所对应的十进制整数。

输入

非负整数N，0 <= N < 10^9

输出

二进制表示的反码所对应的十进制整数

样例输入

```
sample1 input: 
5

sample1 output:
2

解释：5 的二进制表示为 "101"，其二进制反码为 "010"，也就是十进制中的 2 。
```

样例输出

```
sample2 input:
10

sample2 output:
5

解释：10 的二进制表示为 "1010"，其二进制反码为 "0101"，也就是十进制中的 5 。
```

提示

bit manipulation

来源

yan, https://leetcode.cn/problems/complement-of-base-10-integer/



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
class Solution:
    def bitwiseComplement(self, n: int) -> int:
        if n == 0:
            return 1

        # n.bit_length() 返回 n 的二进制有效位数
        mask = (1 << n.bit_length()) - 1
        return mask ^ n  # 或者 return mask - n

if __name__ == "__main__":
    sol = Solution()
    n = int(input())
    print(sol.bitwiseComplement(n))

```

