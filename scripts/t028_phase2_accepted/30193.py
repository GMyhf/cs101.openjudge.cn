# External reference: http://cs101.openjudge.cn/practice/30193/statistics/
# Accepted submission: 52718006
# Source: http://cs101.openjudge.cn/practice/solution/52718006/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, k, b = data[:4]
    total_cells = n * m
    pos = 4

    locked_info = []
    for _ in range(k):
        r, c, t = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        locked_info.append((r - 1, c - 1, t))

    blocked = [False] * total_cells
    for _ in range(b):
        r, c = data[pos], data[pos + 1]
        pos += 2
        blocked[(r - 1) * m + (c - 1)] = True

    total = total_cells - b
    if total <= 0:
        print(-1)
        return

    locked_at = [-1] * (total + 1)
    locked_time = [0] * total_cells
    ok = True

    for r, c, t in locked_info:
        idx = r * m + c
        if not (0 <= r < n and 0 <= c < m) or t < 1 or t > total:
            ok = False
            break
        if blocked[idx] or locked_at[t] != -1:
            ok = False
            break
        if locked_time[idx] != 0:
            ok = False
            break
        locked_at[t] = idx
        locked_time[idx] = t

    start = locked_at[1]
    if not ok or start == -1:
        print(-1)
        return

    neighbors = [[] for _ in range(total_cells)]
    for r in range(n):
        for c in range(m):
            idx = r * m + c
            if blocked[idx]:
                continue
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    nxt = nr * m + nc
                    if not blocked[nxt]:
                        neighbors[idx].append(nxt)

    lock_steps = [t for t in range(1, total + 1) if locked_at[t] != -1]
    next_lock_time = [0] * (total + 1)
    p = 0
    for step in range(total + 1):
        while p < len(lock_steps) and lock_steps[p] <= step:
            p += 1
        next_lock_time[step] = lock_steps[p] if p < len(lock_steps) else 0

    def shortest_distance(src, dst):
        if src == dst:
            return 0
        dist = [-1] * total_cells
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in neighbors[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    if v == dst:
                        return dist[v]
                    q.append(v)
        return -1

    for left, right in zip(lock_steps, lock_steps[1:]):
        dist = shortest_distance(locked_at[left], locked_at[right])
        gap = right - left
        if dist == -1 or dist > gap or (dist & 1) != (gap & 1):
            print(-1)
            return

    visited = [False] * total_cells
    visited[start] = True
    path = [start]

    seen = [0] * total_cells
    dist = [0] * total_cells
    stamp = 0

    def can_still_finish(step, cur):
        nonlocal stamp
        remaining = total - step
        if remaining == 0:
            return True

        target_time = next_lock_time[step]
        target = locked_at[target_time] if target_time else -1
        need = target_time - step if target_time else 0

        if target != -1:
            if visited[target]:
                return False
            cr, cc = divmod(cur, m)
            tr, tc = divmod(target, m)
            manhattan = abs(cr - tr) + abs(cc - tc)
            if manhattan > need or (manhattan & 1) != (need & 1):
                return False

        stamp += 1
        seen[cur] = stamp
        dist[cur] = 0
        q = deque([cur])
        reachable = 0
        target_dist = -1

        while q:
            u = q.popleft()
            for v in neighbors[u]:
                if seen[v] == stamp or visited[v]:
                    continue
                seen[v] = stamp
                dist[v] = dist[u] + 1
                if v == target:
                    target_dist = dist[v]
                reachable += 1
                q.append(v)

        if reachable != remaining:
            return False
        if target != -1 and (target_dist == -1 or target_dist > need):
            return False

        degree_one = 0
        last_locked = locked_at[total]
        for cell in range(total_cells):
            if blocked[cell] or visited[cell]:
                continue

            degree = 0
            only_neighbor = -1
            for nxt_cell in neighbors[cell]:
                if nxt_cell == cur or not visited[nxt_cell]:
                    degree += 1
                    only_neighbor = nxt_cell

            if degree == 0:
                return False
            if degree == 1:
                if only_neighbor == cur and remaining > 1:
                    return False
                if locked_time[cell] not in (0, total):
                    return False
                if last_locked != -1 and cell != last_locked:
                    return False
                degree_one += 1
                if degree_one > 1:
                    return False

        return True

    def onward_degree(cell):
        degree = 0
        next_step = len(path) + 1
        for v in neighbors[cell]:
            if visited[v]:
                continue
            if locked_time[v] and locked_time[v] != next_step:
                continue
            degree += 1
        return degree

    def dfs(step, cur):
        if step == total:
            return True
        if not can_still_finish(step, cur):
            return False

        next_step = step + 1
        fixed = locked_at[next_step]
        if fixed != -1:
            candidates = [fixed] if fixed in neighbors[cur] else []
        else:
            candidates = []
            for v in neighbors[cur]:
                if visited[v]:
                    continue
                if locked_time[v] and locked_time[v] != next_step:
                    continue
                candidates.append(v)
            candidates.sort(key=onward_degree)

        for v in candidates:
            if visited[v]:
                continue
            if locked_time[v] and locked_time[v] != next_step:
                continue

            visited[v] = True
            path.append(v)
            if dfs(next_step, v):
                return True
            path.pop()
            visited[v] = False

        return False

    if dfs(1, start):
        output = []
        for idx in path:
            r, c = divmod(idx, m)
            output.append(f"{r + 1} {c + 1}")
        sys.stdout.write("\n".join(output))
    else:
        print(-1)


if __name__ == "__main__":
    main()
