# 2026-10 审计替换：原 samplecode 是 O(maxw*n*m) 暴力且漏枚举 W>maxw（Y=0 一支），现为二分 W + 前缀和；
# 生成时与 producecase.py 中独立暴力 BRUTE_SOURCE 在全部小组对拍。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
from itertools import accumulate
def main():
    data = sys.stdin.buffer.read().split()
    n, m, S = int(data[0]), int(data[1]), int(data[2])
    w = list(map(int, data[3:3 + 2 * n:2]))
    v = list(map(int, data[4:4 + 2 * n:2]))
    base = 3 + 2 * n
    L = list(map(int, data[base:base + 2 * m:2]))
    R = list(map(int, data[base + 1:base + 2 * m:2]))
    def Y(W):
        c = [0] + list(accumulate(1 if x >= W else 0 for x in w))
        s = [0] + list(accumulate(y if x >= W else 0 for x, y in zip(w, v)))
        return sum((c[r] - c[l - 1]) * (s[r] - s[l - 1]) for l, r in zip(L, R))
    lo, hi = 1, max(w) + 1          # Y(maxw+1)=0<=S，找最小的 W 使 Y(W)<=S
    while lo < hi:
        mid = (lo + hi) // 2
        if Y(mid) <= S:
            hi = mid
        else:
            lo = mid + 1
    ans = S - Y(lo)
    if lo > 1:
        ans = min(ans, Y(lo - 1) - S)
    print(ans)
main()
