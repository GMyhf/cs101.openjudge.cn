# 01729 Jack 参考解。为本仓库判题数据而写的交接产物（2026-09-17），不来自任何外部提交，无外部许可证。
#
# 模型（与 checker.py 一致）：第 0 分钟两人分别在 H、h；此后每分钟没到校的人各走一步（上下左右、
# 不出界、不进 '*'、Jack 不进 h/s、Jill 不进 H/S）；到校即停在校门口不再动，直到两人都到校。
# 路线可以绕路、可以重复经过格子，但一到自己学校路线就结束。要最大化所有整分钟时刻两人距离的最小值。
#
# 做法：状态 (Jack 位置, Jill 位置)。对阈值 thr 判断「只走距离平方 >= thr 的状态能否从 (H,h) 到 (S,s)」，
# 对 thr 在所有可能的距离平方上二分。每个 Jack 位置 a 存一个大整数位集 R[a] 表示 Jill 可达位置，
# Jill 的一步用整行位移实现。最后在最优阈值下分层 BFS，倒推出一对路线。
import sys
from math import sqrt, isqrt


def solve(n, rows):
    size = n * n
    full = (1 << size) - 1
    col_first = 0
    col_last = 0
    for r in range(n):
        col_first |= 1 << (r * n)
        col_last |= 1 << (r * n + n - 1)
    jack_ok = [False] * size
    jill_mask = 0
    for r in range(n):
        for c in range(n):
            ch = rows[r][c]
            i = r * n + c
            if ch == 'H':
                H = i
            elif ch == 'S':
                S = i
            elif ch == 'h':
                h = i
            elif ch == 's':
                s = i
            if ch != '*' and ch not in 'hs':
                jack_ok[i] = True
            if ch != '*' and ch not in 'HS':
                jill_mask |= 1 << i
    sbit = 1 << s
    not_first = full & ~col_first
    not_last = full & ~col_last

    def expand(m):
        return ((m << n) | (m >> n) | ((m & not_last) << 1) | ((m & not_first) >> 1)) & jill_mask

    jack_nbrs = [[] for _ in range(size)]
    for i in range(size):
        if not jack_ok[i] or i == S:
            continue
        r, c = divmod(i, n)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and jack_ok[nr * n + nc]:
                jack_nbrs[i].append(nr * n + nc)
    jack_nbrs[S] = [S]

    def allowed(thr):
        """allowed[a]：Jill 位置 b 满足 dist²(a,b) >= thr 的位集。"""
        res = [0] * size
        for a in range(size):
            if not jack_ok[a]:
                continue
            ar, ac = divmod(a, n)
            close = 0
            for br in range(n):
                rest = thr - 1 - (br - ar) ** 2
                if rest < 0:
                    continue
                w = isqrt(rest)
                lo, hi = max(0, ac - w), min(n - 1, ac + w)
                close |= (((1 << (hi - lo + 1)) - 1) << lo) << (br * n)
            res[a] = jill_mask & ~close
        return res

    def dist2(a, b):
        return (a // n - b // n) ** 2 + (a % n - b % n) ** 2

    def feasible(thr):
        allow = allowed(thr)
        if not (allow[H] >> h) & 1:
            return False
        R = [0] * size
        R[H] = 1 << h
        work = [H]
        queued = [False] * size
        queued[H] = True
        while work:
            a = work.pop()
            queued[a] = False
            m = R[a]
            nxt = expand(m & ~sbit) | (m & sbit)
            for b in jack_nbrs[a]:
                add = nxt & allow[b] & ~R[b]
                if add:
                    R[b] |= add
                    if not queued[b]:
                        queued[b] = True
                        work.append(b)
        return bool(R[S] & sbit)

    cands = sorted({dr * dr + dc * dc for dr in range(n) for dc in range(n)})
    lo, hi = 0, len(cands) - 1          # cands[0] == 0 总可行（题面保证有解）
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(cands[mid]):
            lo = mid
        else:
            hi = mid - 1
    thr = cands[lo]

    # 分层 BFS 并倒推
    allow = allowed(thr)
    seen = [0] * size
    seen[H] = 1 << h
    layers = [{H: 1 << h}]
    while not (seen[S] & sbit):
        frontier = layers[-1]
        new = {}
        for a, m in frontier.items():
            nxt = expand(m & ~sbit) | (m & sbit)
            for b in jack_nbrs[a]:
                add = nxt & allow[b] & ~seen[b]
                if add:
                    seen[b] |= add
                    new[b] = new.get(b, 0) | add
        layers.append(new)
    jack_prev = [[] for _ in range(size)]
    for p in range(size):
        if p != S:
            for q in jack_nbrs[p]:
                jack_prev[q].append(p)

    def jill_prev(b):
        r, c = divmod(b, n)
        res = [s] if b == s else []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            q = nr * n + nc
            if 0 <= nr < n and 0 <= nc < n and q != s and (jill_mask >> q) & 1:
                res.append(q)
        return res

    a, b = S, s
    jack_path, jill_path = [a], [b]
    for t in range(len(layers) - 2, -1, -1):
        layer = layers[t]
        pas = ([S] if a == S else []) + jack_prev[a]
        pbs = jill_prev(b)
        a, b = next((pa, pb) for pa in pas for pb in pbs if (layer.get(pa, 0) >> pb) & 1)
        jack_path.append(a)
        jill_path.append(b)
    jack_path.reverse()
    jill_path.reverse()
    best = min(dist2(x, y) for x, y in zip(jack_path, jill_path))
    assert best == thr
    return "%.2f" % sqrt(thr), moves(jack_path, n), moves(jill_path, n)


def moves(path, n):
    out = []
    for x, y in zip(path, path[1:]):
        if x == y:
            continue
        d = y - x
        out.append('S' if d == n else 'N' if d == -n else 'E' if d == 1 else 'W')
    return "".join(out)


def main():
    data = sys.stdin.read().split()
    p = 0
    blocks = []
    while True:
        n = int(data[p]); p += 1
        if n == 0:
            break
        rows = data[p:p + n]; p += n
        blocks.append((n, rows))
    out = []
    for n, rows in blocks:
        out.append("\n".join(solve(n, rows)))
    print("\n\n".join(out))


main()
