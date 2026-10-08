# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1003: Hangover
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01003/
# License: not declared in source collection; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
import math

while True:
    n = float(input())
    if math.isclose(n, 0.00, rel_tol=1e-5) :
        break

    cnt = 0
    tot = 0
    while  True:
        cnt += 1
        tot += 1/(1+cnt)
        if tot>=n-1e-9:  # 题面要求“至少 c”，c=0.50 恰等于 1/2，须取 1 张
            break

    print(cnt, "card(s)")
