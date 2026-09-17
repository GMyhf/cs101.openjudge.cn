# 30193 哈密顿激活层 参考解。为本仓库判题数据而写的交接产物（2026-09-17），不来自任何外部提交，无外部许可证。
#
# 回溯 + 位集剪枝。网格 <= 10x10，一个格子一位，Python 大整数当位集：
#   静态：黑白染色（路径颜色必须交替）——两色格子数、每个锁定格的颜色与 t 的奇偶；
#         相邻两个锁定点之间的曼哈顿距离不超过时间差。
#   每个结点：
#     · 剩余格子（未访问）必须能从当前位置连通到（位并行洪泛）；
#     · 剩余格子里「在 剩余∪当前 中度数 <= 1」的死胡同最多一个，且只能是终点
#       （若 t=总长 被锁定，只能是那个格子）；
#     · 下一个锁定点在「剩余格子」里的 BFS 距离不超过时间差；
#     · 锁定格只能在自己的时刻进入；下一步被锁定时只能走那一格。
#   候选按「走过去后剩余邻居数」从少到多（Warnsdorff）。
import sys


def main():
    data = sys.stdin.read().split()
    n, m, k, b = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    p = 4
    locks = []
    for _ in range(k):
        locks.append((int(data[p]) - 1, int(data[p + 1]) - 1, int(data[p + 2])))
        p += 3
    blocked = set()
    for _ in range(b):
        blocked.add((int(data[p]) - 1) * m + int(data[p + 1]) - 1)
        p += 2
    path = find_path(n, m, locks, blocked)
    if path is None:
        print(-1)
    else:
        sys.stdout.write("".join(f"{i // m + 1} {i % m + 1}\n" for i in path))


class Budget(Exception):
    pass


def find_path(n, m, locks, blocked, budget=None, tiebreak=None):
    """返回路径（格子编号列表）或 None。造数据时用的两个可选参数：budget 是搜索结点上限，
    超出抛 Budget；tiebreak(格子编号) 给 Warnsdorff 同分候选换一种次序。"""
    size = n * m
    total = size - len(blocked)
    free = 0
    for i in range(size):
        if i not in blocked:
            free |= 1 << i
    lock_at = {}
    lock_time = {}
    for r, c, t in locks:
        i = r * m + c
        if i in blocked or not (1 <= t <= total) or t in lock_at or i in lock_time:
            return None
        lock_at[t] = i
        lock_time[i] = t
    if 1 not in lock_at:
        return None
    start = lock_at[1]
    color = lambda i: (i // m + i % m) & 1
    same = sum(1 for i in range(size) if i not in blocked and color(i) == color(start))
    if same != (total + 1) // 2:
        return None
    for t, i in lock_at.items():
        if (color(i) == color(start)) != (t % 2 == 1):
            return None
    times = sorted(lock_at)
    for t1, t2 in zip(times, times[1:]):
        a, c = lock_at[t1], lock_at[t2]
        if abs(a // m - c // m) + abs(a % m - c % m) > t2 - t1:
            return None
    if total == 1:
        return [start]

    left_col = 0
    right_col = 0
    for r in range(n):
        left_col |= 1 << (r * m)
        right_col |= 1 << (r * m + m - 1)
    no_left = ((1 << size) - 1) & ~left_col
    no_right = ((1 << size) - 1) & ~right_col

    def up(x):
        return x >> m

    def down(x):
        return (x << m) & free

    def west(x):
        return (x & no_left) >> 1

    def east(x):
        return (x & no_right) << 1

    def expand(x):
        return ((x >> m) | (x << m) | ((x & no_left) >> 1) | ((x & no_right) << 1)) & free

    nbrs = []
    for i in range(size):
        r, c = divmod(i, m)
        lst = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and (nr * m + nc) not in blocked:
                lst.append(nr * m + nc)
        nbrs.append(lst)

    next_lock = [0] * (total + 2)   # next_lock[s] = 最小的锁定时刻 > s（没有则 0）
    nxt = 0
    for s in range(total, -1, -1):
        next_lock[s] = nxt
        if s in lock_at:
            nxt = s
    end_cell = lock_at.get(total, -1)
    locked_mask = 0
    for i in lock_time:
        locked_mask |= 1 << i
    path = [start]

    def feasible(step, cur, rest):
        # rest：未访问格子（不含 cur）；step：cur 是第 step 步
        if not rest:
            return True
        # 连通
        reach = expand(1 << cur) & rest
        if not reach:
            return False
        while True:
            more = (reach | expand(reach)) & rest
            if more == reach:
                break
            reach = more
        if reach != rest:
            return False
        # 死胡同
        live = rest | (1 << cur)
        # 格子 x 在 live 中的邻居：x 上方在 live ⇔ x ∈ down(live)
        n1, n2, n3, n4 = down(live), up(live), east(live), west(live)
        two = (n1 & n2) | (n1 & n3) | (n1 & n4) | (n2 & n3) | (n2 & n4) | (n3 & n4)
        dead = rest & ~two
        if dead:
            if dead & (dead - 1):
                return False
            if end_cell >= 0:
                if dead != 1 << end_cell:
                    return False
            elif dead & locked_mask:
                return False
            # 唯一邻居是 cur 的死胡同必须下一步就走、又必须是终点
            if dead != rest and not (dead & (up(rest) | down(rest) | east(rest) | west(rest))):
                return False
        # 下一个锁定点的距离
        t = next_lock[step]
        if t:
            target = 1 << lock_at[t]
            gap = t - step
            frontier = 1 << cur
            seen = frontier
            dist = 0
            while not (frontier & target):
                dist += 1
                if dist > gap:
                    return False
                frontier = expand(frontier) & rest & ~seen
                if not frontier:
                    return False
                seen |= frontier
        return True

    sys.setrecursionlimit(10000)

    calls = [0]

    def dfs(step, cur, rest):
        if step == total:
            return True
        calls[0] += 1
        if budget is not None and calls[0] > budget:
            raise Budget()
        if not feasible(step, cur, rest):
            return False
        s1 = step + 1
        forced = lock_at.get(s1)
        if forced is not None:
            cands = [forced] if (rest >> forced) & 1 and forced in nbrs[cur] else []
        else:
            cands = [v for v in nbrs[cur] if (rest >> v) & 1 and v not in lock_time]
            if len(cands) > 1:
                if tiebreak is None:
                    cands.sort(key=lambda v: sum(1 for w in nbrs[v] if (rest >> w) & 1))
                else:
                    cands.sort(key=lambda v: (sum(1 for w in nbrs[v] if (rest >> w) & 1), tiebreak(v)))
        for v in cands:
            path.append(v)
            if dfs(s1, v, rest & ~(1 << v)):
                return True
            path.pop()
        return False

    if dfs(1, start, free & ~(1 << start)):
        return path
    return None


if __name__ == "__main__":
    main()
