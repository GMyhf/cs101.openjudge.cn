# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1065: Wooden Sticks
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01065/
# License: not declared in source collection; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：原先的 2020fall 贪心（排序后反复扫链）是对的，但最坏 O(n^2)；数据放大到 n=5000 后换成
# Dilworth：按 (l, w) 升序排好后，所需准备次数 = w 序列的最长严格下降子序列长度，O(n log n)。
import sys
from bisect import bisect_left
tok = sys.stdin.read().split()
T = int(tok[0]); p = 1; out = []
for _ in range(T):
    n = int(tok[p]); p += 1
    a = sorted((int(tok[p + 2 * i]), int(tok[p + 2 * i + 1])) for i in range(n)); p += 2 * n
    tails = []                       # 对 -w 求最长严格上升子序列
    for _, w in a:
        x = -w
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x
    out.append(str(len(tails)))
print("\n".join(out))
