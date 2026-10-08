# External reference: http://cs101.openjudge.cn/practice/02157/statistics/
# Accepted submission: 45991187
# Source: http://cs101.openjudge.cn/practice/solution/45991187/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 修正版参考解（2026-10 数据审计）：原 Accepted 提交只按 A..E 顺序尝试开门一轮，
# 开 B 门后才拿齐 A 门钥匙时不会回头再开 A，会把 YES 判成 NO。这里反复 BFS 直到不再有新门可开。
import sys
from collections import deque

def solve(g, h, w):
    total = {}
    for row in g:
        for c in row:
            if 'a' <= c <= 'e':
                total[c] = total.get(c, 0) + 1
    for i in range(h):
        for j in range(w):
            if g[i][j] == 'S':
                si, sj = i, j
    opened = set()
    while True:
        seen = [[False] * w for _ in range(h)]
        seen[si][sj] = True
        q = deque([(si, sj)])
        got = {}
        while q:
            i, j = q.popleft()
            c = g[i][j]
            if c == 'G':
                return True
            if 'a' <= c <= 'e':
                got[c] = got.get(c, 0) + 1
            for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                if 0 <= x < h and 0 <= y < w and not seen[x][y]:
                    d = g[x][y]
                    if d == 'X' or ('A' <= d <= 'E' and d not in opened):
                        continue
                    seen[x][y] = True
                    q.append((x, y))
        new = {d for d in 'ABCDE' if d not in opened and total.get(d.lower(), 0) > 0
               and got.get(d.lower(), 0) == total[d.lower()]}
        if not new:
            return False
        opened |= new

def main():
    t = sys.stdin.read().split()
    p = 0
    out = []
    while p + 1 < len(t):
        h, w = int(t[p]), int(t[p + 1]); p += 2
        if h == 0 and w == 0:
            break
        g = t[p:p + h]; p += h
        out.append('YES' if solve(g, h, w) else 'NO')
    print('\n'.join(out))

main()
