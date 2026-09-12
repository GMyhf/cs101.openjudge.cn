#!/usr/bin/env python3
"""01830 开关问题 —— 参考实现（仓库交接件，非平台提交，不套用外部许可）。

操作第 i 个开关会翻转它自己，再翻转题面里每条 `I J`（I=i）指到的第 J 个。所以第 j
个开关的终态只由「操作了自己」和「操作了所有指向它的开关」决定，在 GF(2) 上就是

    x_j + Σ_{(i,j)∈E} x_i ≡ start_j ⊕ target_j

**对角线那一项 x_j 是输入里永远不会出现的**（题面只给关联关系，不给「开关翻转自己」
这件事）—— 漏掉它整题就错：题面样例第一组会从 4 变成 impossible。2026-09-12 之前
这份参考实现正是漏了它，21 组数据全是错的答案，见 CHANGELOG。

每个开关最多操作一次，所以答案就是解的个数：消元后若出现「0 = 1」则无解，
否则自由变量有 n-rank 个，答案 2^(n-rank)。
"""
import sys

IMPOSSIBLE = "Oh,it's impossible~!!"


def one_case(n, start, target, edges):
    # rows[j] 低 n 位是第 j 行系数，第 n 位是右端项；对角线先置上再叠加入边。
    rows = []
    for j in range(n):
        mask = 1 << j
        for i, k in edges:
            if k == j:
                mask |= 1 << i
        rows.append(mask | (((start[j] ^ target[j]) & 1) << n))
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, n) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(n):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
    if any((row & ((1 << n) - 1)) == 0 and ((row >> n) & 1) for row in rows):
        return IMPOSSIBLE
    return str(1 << (n - rank))


def solve(text):
    it = iter(text.split())
    k = int(next(it)); answers = []
    for _ in range(k):
        n = int(next(it))
        if n == 0: break
        start = [int(next(it)) for _ in range(n)]; target = [int(next(it)) for _ in range(n)]
        edges = []
        while True:
            i, j = int(next(it)), int(next(it))
            if i == j == 0: break
            edges.append((i - 1, j - 1))
        answers.append(one_case(n, start, target, edges))
    return '\n'.join(answers) + ('\n' if answers else '')


if __name__ == '__main__':
    sys.stdout.write(solve(sys.stdin.read()))
