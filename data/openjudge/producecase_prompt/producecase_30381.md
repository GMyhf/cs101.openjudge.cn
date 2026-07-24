请根据生成数据的模版 producecase_template.py，以及能够AC的代码ac.py，给出下面这个题目的生产数据的 producecase.py

2026 年，动物城迎来了盛大的马年春节！动物城的市长马飞扬对这个本命年充满了执念，他决定要“大展马威，有所作为”。他亲自策划了一场史无前例的集卡活动，名为“集 N 星颂马年”。

你需要集齐一套完整的 **N 种不同的动物城明星卡片**（例如：兔朱迪、狐尼克、夏奇羊等），才能向市政府兑换马飞扬市长的亲笔签名照一张。马市长为此专门聘请了数百万替身来签名，所以签名照数量无限，但兑换卡片严格要求：每兑换一份签名照，需要每种明星卡各一张。

活动中有一种特殊的卡片，名为**万能卡**（据说是马市长通过特殊渠道获得的），它可以替代兑换所需的**任意一张**明星卡。但为了其他卡牌（尤其是自己的卡牌）能更好地流通，马市长规定**一套卡组至多使用一张万能卡**。

现在，你拥有第 i 种明星卡 ci 张，以及万能卡 M 张。你的任务是利用手头的所有卡片，集齐**数量最多**的完整套卡，以兑换最多的马市长亲笔签名照。每张卡片（明星卡或万能卡）最多只能使用一次。

输入

第一行包含两个整数 N, M，分别表示明星卡的种类数和万能卡的张数。
第二行包含 N 个整数 c1, c2, ... ，cN, 表示每种明星卡的张数。
数据满足：2<=N<=50, 0<=M, ci<=500,000,000。

输出

输出仅一个整数，即最多可以兑换的马飞扬市长亲笔签名照数目。

样例输入

```
3 4
1 2 3
```

样例输出

```
3
```

提示

输入数据表明：一共有 1 张明星卡 1，2 张明星卡 2，3 张明星卡 3，以及 4 张万能卡。最多可以集齐三套卡片。套组 1: {万能卡, 明星卡 2, 明星卡 3}，套组 2: {万能卡, 明星卡 2, 明星卡 3}，套组 3: {明星卡 1, 万能卡, 明星卡 3}。



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

def check(x, n, m, cards):
    """
    判断是否能集齐 x 套卡组
    """
    # total_needed 表示为了凑齐 x 套，总共需要多少张万能卡
    total_needed = 0
    for c in cards:
        if c < x:
            total_needed += (x - c)
    
    # 条件 1：需要的万能卡总数不能超过手里的万能卡 M
    # 条件 2：每套卡组最多只能用 1 张万能卡，所以 X 套卡组最多只能消耗 X 张万能卡
    if total_needed <= m and total_needed <= x:
        return True
    return False

def solve():
    # 读取第一行 N 和 M
    try:
        line1 = sys.stdin.readline().split()
        if not line1:
            return
        n = int(line1[0])
        m = int(line1[1])
        
        # 读取第二行各明星卡的数量
        line2 = sys.stdin.readline().split()
        if not line2:
            cards = []
        else:
            cards = [int(x) for x in line2]
    except EOFError:
        return

    # 二分查找的范围
    # 最小 0 套，最大可能是原有卡片最大值加上万能卡（设定为 10 亿足够）
    low = 0
    high = 1000000000
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid, n, m, cards):
            ans = mid      # 如果 mid 套可行，记录答案并尝试更大的数
            low = mid + 1
        else:
            high = mid - 1 # 如果不可行，尝试更小的数
            
    print(ans)

if __name__ == "__main__":
    solve()
```

