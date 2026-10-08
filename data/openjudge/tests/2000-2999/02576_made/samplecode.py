# External reference: http://cs101.openjudge.cn/practice/02576/statistics/
# Accepted submission: 41410928
# Source: http://cs101.openjudge.cn/practice/solution/41410928/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：按人数分层的位集背包。原内嵌参考解（Accepted submission 41410928）在 n=100 时约 1e8 次
# Python 循环跑不动满规模数据，且 n 为奇数时只在 ceil(n/2) 人的队里找会漏掉最优解，故换成此写法（已与穷举对拍）。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
data = sys.stdin.read().split()
n = int(data[0]); w = list(map(int, data[1:1 + n]))
S = sum(w); k = n // 2
dp = [0] * (k + 1); dp[0] = 1
for x in w:
    for c in range(k, 0, -1):
        dp[c] |= dp[c - 1] << x
best = None
for v, ch in enumerate(bin(dp[k])[:1:-1]):
    if ch == "1" and (best is None or abs(2 * v - S) < abs(2 * best - S)):
        best = v
a, b = best, S - best
print(min(a, b), max(a, b))
