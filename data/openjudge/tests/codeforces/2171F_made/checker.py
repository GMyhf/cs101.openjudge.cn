"""Codeforces 2171F checker (answers are not unique).

Written for this repository as a hand-off artifact; no external license.
python3 -I checker.py <input> <contestant_output> <reference_answer>; exit 0 = AC, 42 = WA.

Existence is decided here, independently of the reference file: a tree exists iff the
graph {u<v, pos(u)<pos(v)} is connected iff for every split k (1 <= k < n)
min(p_1..p_k) < max(p_{k+1}..p_n).  Per test the contestant must print Yes/No (any
letter case) matching that decision; after Yes exactly n-1 pairs "u v" (either order)
with 1 <= u, v <= n, u != v, the smaller one placed earlier in p, and no pair closing a
cycle (n-1 acyclic edges on n vertices = spanning tree).  Nothing may follow the last test.
"""
import sys


def wa(msg):
    print(msg)
    sys.exit(42)


def to_int(tok):
    if not 0 < len(tok) <= 12:
        return None
    s = tok[1:] if tok[:1] == b"-" else tok
    if not s or not s.isdigit():
        return None
    return int(tok)


def main():
    inp = open(sys.argv[1], "rb").read().split()
    with open(sys.argv[2], "rb") as f:
        out = f.read().split()
    total = len(out)
    t = int(inp[0]); ip = 1; p = 0
    for case in range(1, t + 1):
        n = int(inp[ip]); ip += 1
        perm = [int(x) for x in inp[ip:ip + n]]; ip += n
        pos = [0] * (n + 1)
        for i, v in enumerate(perm):
            pos[v] = i
        exists = True
        mn = n + 1
        sufmax = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            sufmax[i] = max(sufmax[i + 1], perm[i])
        for k in range(n - 1):
            if perm[k] < mn:
                mn = perm[k]
            if mn > sufmax[k + 1]:
                exists = False
                break
        if p >= total:
            wa(f"第 {case} 组测试：输出不完整")
        word = out[p].lower(); p += 1
        if word not in (b"yes", b"no"):
            wa(f"第 {case} 组测试：应输出 Yes 或 No")
        if word == b"no":
            if exists:
                wa(f"第 {case} 组测试：满足条件的树存在，却输出了 No")
            continue
        if not exists:
            wa(f"第 {case} 组测试：满足条件的树不存在，却输出了 Yes")
        if p + 2 * (n - 1) > total:
            wa(f"第 {case} 组测试：边数不足 n-1 条")
        parent = list(range(n + 1))
        for _ in range(n - 1):
            u = to_int(out[p]); v = to_int(out[p + 1]); p += 2
            if u is None or v is None or not (1 <= u <= n and 1 <= v <= n):
                wa(f"第 {case} 组测试：边的端点不是 1..n 内的整数")
            if u == v:
                wa(f"第 {case} 组测试：边的两个端点相同")
            if u > v:
                u, v = v, u
            if pos[u] > pos[v]:
                wa(f"第 {case} 组测试：有一条边的较小端点在排列中出现在较大端点之后")
            a = u
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            b = v
            while parent[b] != b:
                parent[b] = parent[parent[b]]; b = parent[b]
            if a == b:
                wa(f"第 {case} 组测试：给出的边成环或重复，不是一棵树")
            parent[a] = b
    if p != total:
        wa("输出里有多余的内容")
    sys.exit(0)


main()
