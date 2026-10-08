# External reference: http://cs101.openjudge.cn/practice/01084/statistics/
# Accepted submission: 45386897
# Source: http://cs101.openjudge.cn/practice/solution/45386897/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法用布尔列表表示状态，每次估价都 deepcopy 并逐根火柴检查，n=5 火柴齐全时要跑一分钟以上；
# 现改为位掩码表示火柴与正方形、按边长从小到大枚举，仍是 IDA*（迭代加深 + 贪心估价），单次估价 O(正方形数)。

import sys


def estimate(g):
    # 乐观估价：贪心找出互不共享已删火柴的完好正方形，每个至少还要删一根
    cnt = 0
    for s in squares:
        if not s & g:
            cnt += 1
            g |= s
    return cnt


def dfs(g, t):
    est = estimate(g)
    if t + est > limit:
        return False
    if est == 0:
        return True
    for s in squares:
        if not s & g:
            break
    for b in sticks[s]:
        if dfs(g | b, t + 1):
            return True
    return False


data = sys.stdin.read().split()
pos = 1
out = []
for _ in range(int(data[0])):
    n = int(data[pos])
    m = int(data[pos + 1])
    nums = data[pos + 2:pos + 2 + m]
    pos += 2 + m
    d = 2 * n + 1
    squares = []
    for k in range(1, n + 1):
        for i in range(n):
            for j in range(n):
                if i + k <= n and j + k <= n:
                    mask = 0
                    for p in range(1, k + 1):
                        for y in (d*i+j+p, d*(i+p)+j-n, d*(i+p)+j-n+k, d*(i+k)+j+p):
                            mask |= 1 << y
                    squares.append(mask)
    sticks = {s: [1 << y for y in range(s.bit_length()) if s >> y & 1] for s in squares}
    judge = 0
    for num in nums:
        judge |= 1 << int(num)
    limit = estimate(judge)
    while not dfs(judge, 0):
        limit += 1
    out.append(str(limit))
print('\n'.join(out))
