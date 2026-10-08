# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2979: 陪审团的人选
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02979/
# License: not declared; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 陪审团的人选（POJ 1015）参考解：按候选人逐个做 0/1 背包，
# dp[j][k] = 选 j 人、控辩差偏移为 k 时的最大控辩和；保存每步快照用于回溯成员。
# 旧参考解是经典的「f[j][k] + 沿 path 查重」写法，它只保留每个状态的一条路径，
# 在少数数据上会漏掉最优方案（不满足最优子结构），故换成这个精确解。
import sys
def solve(n, m, P, D):
    off = 20 * m; W = 2 * off + 1
    dp = [[-1] * W for _ in range(m + 1)]; dp[0][off] = 0; snaps = []
    for i in range(n):
        s = P[i] + D[i]; t = P[i] - D[i]
        snaps.append([row[:] for row in dp])
        for j in range(min(i + 1, m), 0, -1):
            prev = dp[j - 1]; cur = dp[j]; r = 20 * (j - 1)
            for k in range(off - r, off + r + 1):
                v = prev[k]
                if v >= 0 and v + s > cur[k + t]: cur[k + t] = v + s
    for diff in range(off + 1):
        ks = [k for k in sorted({off + diff, off - diff}) if dp[m][k] >= 0]
        if ks:
            k = max(ks, key=lambda x: dp[m][x]); break
    j = m; val = dp[m][k]; members = []
    for i in range(n - 1, -1, -1):
        if j == 0: break
        if snaps[i][j][k] == val: continue
        members.append(i + 1); j -= 1; k -= P[i] - D[i]; val -= P[i] + D[i]
    members.reverse(); return members
def main():
    data = list(map(int, sys.stdin.read().split())); p = 0; case = 0; out = []
    while True:
        n, m = data[p], data[p + 1]; p += 2
        if n == 0 and m == 0: break
        P = data[p:p + 2 * n:2]; D = data[p + 1:p + 2 * n:2]; p += 2 * n; case += 1
        mem = solve(n, m, P, D)
        out.append(f"Jury #{case}")
        out.append(f"Best jury has value {sum(P[i-1] for i in mem)} for prosecution and value {sum(D[i-1] for i in mem)} for defence:")
        out.append("".join(f" {i}" for i in mem)); out.append("")
    print("\n".join(out))
main()
