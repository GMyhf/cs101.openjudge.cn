# External reference: statistics page /practice/21532/
# Accepted submission: 52201278
# Source: http://cs101.openjudge.cn/practice/solution/52201278/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原外部参考（提交 52201278）从 6 逐个试到最小因子，N 为接近 1e9 的质数时要循环约 1e9 次，
# 生成满规模数据会超时，改为 O(sqrt N) 枚举因子：答案 = N / (N 的不小于 6 的最小因子)。
n = int(input())
best = n
i = 1
while i * i <= n:
    if n % i == 0:
        for d in (i, n // i):
            if d >= 6 and d < best:
                best = d
    i += 1
print(n // best)
