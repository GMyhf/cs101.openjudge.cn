# 2026-10 审计替换：原 samplecode 是把 k 个加速器全部分配的指数暴力，跑不动题面规模；现为成批贪心 O(n^2)。
# 生成时与 producecase.py 中的原暴力 BRUTE_SOURCE（小组）及逐个贪心 GREEDY1_SOURCE（中组）对拍。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
def main():
    a = sys.stdin.buffer.read().split()
    n, m, k = int(a[0]), int(a[1]), int(a[2])
    D = [0] + [int(x) for x in a[3:3 + n - 1]]          # D[i]: i -> i+1
    p = 3 + n - 1
    last = [0] * (n + 2)                                 # 站点最晚到达乘客时刻
    down = [0] * (n + 2)                                 # 在该站下车人数
    sumT = 0
    for _ in range(m):
        t, x, y = int(a[p]), int(a[p + 1]), int(a[p + 2]); p += 3
        if t > last[x]:
            last[x] = t
        down[y] += 1
        sumT += t
    arr = [0] * (n + 2)
    def compute():
        arr[1] = 0
        for i in range(1, n):
            arr[i + 1] = max(arr[i], last[i]) + D[i]
    compute()
    while k > 0:
        # far[i]: 从站 i 起，到达时间的减少能一直传到的最远站（arr[j]>last[j] 时继续传）
        best = 0; bi = -1; bslack = 0
        reach = 0; slack = 0; ben = 0
        # 从后往前：g[j] = 若站 j 到达提前 1，受益的下车人数；以及传播链上最小松弛
        g = [0] * (n + 2); sl = [0] * (n + 2)
        g[n] = down[n]; sl[n] = 1 << 60
        for j in range(n - 1, 1, -1):
            if arr[j] > last[j]:
                g[j] = down[j] + g[j + 1]
                s = arr[j] - last[j]
                sl[j] = s if s < sl[j + 1] else sl[j + 1]
            else:
                g[j] = down[j]; sl[j] = 1 << 60
        for i in range(1, n):
            if D[i] > 0 and g[i + 1] > best:
                best = g[i + 1]; bi = i
        if bi < 0:
            break
        # 站 i+1 的到达提前不受 i+1 自身松弛约束（传播到 i+2 才需要 arr[i+1]>last[i+1]）
        j = bi + 1
        lim = sl[j] if j <= n - 1 and arr[j] > last[j] else 1 << 60
        use = min(k, D[bi], lim)
        D[bi] -= use; k -= use
        compute()
    total = 0
    p = 3 + n - 1
    for _ in range(m):
        y = int(a[p + 2]); p += 3
        total += arr[y]
    print(total - sumT)
main()
