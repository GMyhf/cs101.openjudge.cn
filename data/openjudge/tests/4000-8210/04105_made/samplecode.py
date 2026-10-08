# 2026-10 审计替换：原多题合一脚本里的 r4105 用普通 BFS 处理 0 代价传送（队列失序、答案偏大），
# 且把「集齐 K 种」当成「集齐图上出现过的种类」。现与 producecase.py 的 REFERENCE 相同（分层 BFS + 传送门闭包）。
import sys


def solve(R, C, K, g):
    cells = "".join(g)
    n = R * C
    full = (1 << K) - 1
    gem = [0] * n
    for i, ch in enumerate(cells):
        if "0" <= ch <= "4" and int(ch) < K:
            gem[i] = 1 << int(ch)
    portals = [i for i, ch in enumerate(cells) if ch == "$"]
    isp = [ch == "$" for ch in cells]
    nb = []
    for i in range(n):
        r, c = divmod(i, C)
        lst = []
        if cells[i] != "#":
            if r > 0 and cells[i - C] != "#": lst.append(i - C)
            if r < R - 1 and cells[i + C] != "#": lst.append(i + C)
            if c > 0 and cells[i - 1] != "#": lst.append(i - 1)
            if c < C - 1 and cells[i + 1] != "#": lst.append(i + 1)
        nb.append(lst)
    s = cells.index("S"); e = cells.index("E")
    target = (e << 5) | full
    seen = bytearray(n << 5)
    start = s << 5
    seen[start] = 1
    frontier = [start]
    d = 0
    while frontier:
        k = 0
        while k < len(frontier):  # 同层内传送门 0 代价闭包
            st = frontier[k]; k += 1
            if st == target:
                return str(d)
            cell = st >> 5
            if isp[cell]:
                m = st & 31
                for p in portals:
                    t = (p << 5) | m
                    if not seen[t]:
                        seen[t] = 1; frontier.append(t)
        nxt = []
        for st in frontier:
            m = st & 31
            for j in nb[st >> 5]:
                t = (j << 5) | (m | gem[j])
                if not seen[t]:
                    seen[t] = 1; nxt.append(t)
        frontier = nxt
        d += 1
    return "oop!"


def main():
    a = sys.stdin.read().split()
    t = int(a[0]); i = 1; out = []
    for _ in range(t):
        R, C, K = int(a[i]), int(a[i + 1]), int(a[i + 2]); i += 3
        g = a[i:i + R]; i += R
        out.append(solve(R, C, K, g))
    print("\n".join(out))


main()
