# External reference: http://cs101.openjudge.cn/practice/01129/statistics/
# Accepted submission: 52288382
# Source: http://cs101.openjudge.cn/practice/solution/52288382/
# License: not declared on the submission page; no license is inferred.
# 注：原提交的回溯只在全部着色后才检查冲突，n=26 时指数爆炸；改为 DSATUR 剪枝回溯。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。

import sys
sys.setrecursionlimit(10000)
def min_channels(n, adj):
    # DSATUR 回溯：每次选饱和度最大的未着色点，只试与邻居不冲突的颜色
    for k in range(1, 5):
        col = [-1] * n
        def bt(cnt):
            if cnt == n:
                return True
            best = -1; bs = -1; bd = -1
            for v in range(n):
                if col[v] < 0:
                    s = len({col[u] for u in adj[v] if col[u] >= 0})
                    if s > bs or (s == bs and len(adj[v]) > bd):
                        best, bs, bd = v, s, len(adj[v])
            used = {col[u] for u in adj[best]}
            for c in range(k):
                if c not in used:
                    col[best] = c
                    if bt(cnt + 1):
                        return True
            col[best] = -1
            return False
        if bt(0):
            return k
    return 4
tok = sys.stdin.read().split()
p = 0
out = []
while True:
    n = int(tok[p]); p += 1
    if n == 0:
        break
    adj = [set() for _ in range(n)]
    for i in range(n):
        s = tok[p]; p += 1
        for ch in s.split(':', 1)[1]:
            j = ord(ch) - 65
            adj[i].add(j); adj[j].add(i)
    k = min_channels(n, adj)
    out.append(f"{k} channel needed." if k == 1 else f"{k} channels needed.")
print('\n'.join(out))
