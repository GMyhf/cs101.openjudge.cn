# External reference: http://cs101.openjudge.cn/practice/01050/statistics/
# Accepted submission: 50936084
# Source: http://cs101.openjudge.cn/practice/solution/50936084/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：原先引用的提交（50936084）只枚举上边界 j<i 的行段 j+1..i，漏掉了从第 0 行开始的子矩形，
# N=1 时输出 -inf；旧生成器靠「第一行全负」把这个缺陷藏住了。这里换成 O(N^3) 的列压缩 + Kadane。
import sys
data = sys.stdin.buffer.read().split()
n = int(data[0])
a = list(map(int, data[1:1 + n * n]))
rows = [a[i * n:(i + 1) * n] for i in range(n)]
best = -10 ** 18
for top in range(n):
    col = [0] * n
    for bot in range(top, n):
        col = [c + v for c, v in zip(col, rows[bot])]
        cur = 0
        m = -10 ** 18
        for c in col:
            cur = c if cur < 0 else cur + c
            if cur > m:
                m = cur
        if m > best:
            best = m
print(best)
