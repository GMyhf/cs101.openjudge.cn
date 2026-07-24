请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py。



## 最大连续答案

sliding window, http://dsbpython.openjudge.cn/2026moni1re/011/

> 给定一个长度不超过20000的由'T'或'F'构成的字符串，允许修改字符最多k次（将'T'改成'F'或将'F'改成'T')，问能得到的最长的连续相同字符字串长度是多少。
>
> **输入**
>
> 第1行，一个由'T'或'F'构成的字符串
> 第2行：整数k (0 <= k <= 第1行字符串长度）
>
> **输出**
>
> 答案
>
> 样例输入
>
> ```
> TTFF
> 2
> ```
>
> 样例输出
>
> ```
> 4
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
def solve():
    s = sys.stdin.readline().strip()
    k = int(sys.stdin.readline())
    ans = 0
    for target in ('T', 'F'):
        l = cnt = 0
        for r in range(len(s)):
            if s[r] != target:
                cnt += 1
            while cnt > k:
                if s[l] != target:
                    cnt -= 1
                l += 1
            ans = max(ans, r - l + 1)
    print(ans)

if __name__ == "__main__":
    import sys
    solve()
```

