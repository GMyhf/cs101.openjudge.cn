# External reference: statistics page /practice/21516/
# Accepted submission: 47436368
# Source: http://cs101.openjudge.cn/practice/solution/47436368/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原外部参考 http://cs101.openjudge.cn/practice/solution/47436368/ 在含反向边的图上答案错误（如 data/40.in 给 113，正确为 221），
# 已换成与 producecase.py 内嵌 REFERENCE 相同的迭代并查集解（已与暴力模拟对拍）。

# 迭代并查集写法（原外部 AC 代码递归找组，N=1e5 的长链会爆栈/超时，换成本解；小规模已与原 AC 代码和暴力模拟对拍一致）
import sys
def main():
    d = sys.stdin.buffer.read().split(); n, m = int(d[0]), int(d[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        adj[int(d[2 + 2 * i])].append(int(d[3 + 2 * i]))
    par = list(range(n + 1)); sz = [1] * (n + 1); members = [[v] for v in range(n + 1)]
    queue = []
    def find(x):
        r = x
        while par[r] != r: r = par[r]
        while par[x] != r: par[x], x = r, par[x]
        return r
    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return
        if sz[a] < sz[b]: a, b = b, a
        if sz[a] == 1: queue.append(a)
        if sz[b] == 1: queue.append(b)
        par[b] = a; sz[a] += sz[b]; members[a].extend(members[b]); members[b] = []
    # 同一个点的所有出边终点两两开会，并成一组
    for x in range(1, n + 1):
        for y in adj[x][1:]: union(adj[x][0], y)
    # 组大小>=2 时组内成团，组内任一点的出边终点都会被拉进组
    while queue:
        v = queue.pop()
        for y in adj[v]: union(v, y)
    ans = 0
    for v in range(1, n + 1):
        if par[v] == v and sz[v] >= 2: ans += sz[v] * (sz[v] - 1)
        elif sz[find(v)] == 1: ans += len(adj[v])
    print(ans)
main()
