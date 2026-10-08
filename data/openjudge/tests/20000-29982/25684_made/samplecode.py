# External reference: statistics page /practice/25684/
# Accepted submission: 51527327
# Source: http://cs101.openjudge.cn/practice/solution/51527327/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原代码开 10^6+1 的时刻数组逐时刻累加：s+d 可到 2×10^6 会越界，满规模时累加上亿次也会超时。
# 改为扫描线：到达 +n、离开 -n，同一时刻先离开后到达。

m, c = map(int, input().split())
events = []
for _ in range(m):
    n, s, d = map(int, input().split())
    if d:
        events.append((s, n))
        events.append((s+d, -n))
events.sort()
cur = 0
ok = True
for _, v in events:
    cur += v
    if cur > c:
        ok = False
        break
print('Y' if ok else 'N')
