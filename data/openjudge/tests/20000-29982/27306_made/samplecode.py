# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 原样例解只检查“相同”连通块内有无“不同”结论，漏判“不同”构成的奇环（如三株两两不同），已改为带权并查集，与 producecase.py 的 REFERENCE_SOURCE 一致。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
sys.setrecursionlimit(10000)
data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
parent = list(range(n))
rel = [0] * n  # rel[x]: x 与 parent[x] 是否不同种类


def find(x):
    if parent[x] == x:
        return x
    root = find(parent[x])
    rel[x] ^= rel[parent[x]]
    parent[x] = root
    return root


ok = True
for k in range(m):
    a, b, c = int(data[2 + 3 * k]), int(data[3 + 3 * k]), int(data[4 + 3 * k])
    ra, rb = find(a), find(b)
    if ra == rb:
        if rel[a] ^ rel[b] != c:
            ok = False
            break
    else:
        parent[rb] = ra
        rel[rb] = rel[a] ^ rel[b] ^ c
print('YES' if ok else 'NO')
