# External reference: http://cs101.openjudge.cn/practice/02373/statistics/
# Accepted submission: 43079895
# Source: http://cs101.openjudge.cn/practice/solution/43079895/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法对每头牛逐格标记区间内部，最坏 O(N*L)≈10^9 次赋值，满规模超时；另用 input 逐行读入。
# 新写法：差分数组标记牛区间内部 O(N+L)，DP 只在偶数点上做，用单调队列维护窗口 [i-2B, i-2A] 最小值，总 O(N+L)。

import sys
from collections import deque

data = sys.stdin.buffer.read().split()
n, l, a, b = int(data[0]), int(data[1]), int(data[2]), int(data[3])
diff = [0] * (l + 2)
for k in range(n):
    s, e = int(data[4 + 2 * k]), int(data[5 + 2 * k])
    diff[s + 1] += 1    # 牛区间 (s, e) 内部不能作为喷头分界点
    diff[e] -= 1
cow = [False] * (l + 1)
c = 0
for i in range(l + 1):
    c += diff[i]
    cow[i] = c > 0

INF = float('inf')
d = [INF] * (l + 1)     # d[i]：恰好覆盖 [0, i] 所需最少喷头数
d[0] = 0
a2 = a * 2
b2 = b * 2
q = deque()             # 存下标，对应 d 值单调不减
for i in range(a2, l + 1, 2):
    j = i - a2          # 新进入窗口的左端点
    if d[j] < INF:
        while q and d[q[-1]] >= d[j]:
            q.pop()
        q.append(j)
    while q and q[0] < i - b2:
        q.popleft()
    if q and not cow[i]:
        d[i] = d[q[0]] + 1
print(d[l] if d[l] < INF else -1)
