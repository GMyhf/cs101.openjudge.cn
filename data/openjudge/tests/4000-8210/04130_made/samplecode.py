# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
import heapq
from collections import deque

def solve():
    data = sys.stdin.read().splitlines()
    if not data:
        return
    line_index = 0
    # 四个方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    results = []
    
    while line_index < len(data):
        if not data[line_index].strip():
            line_index += 1
            continue
        parts = data[line_index].split()
        line_index += 1
        n = int(parts[0])
        m = int(parts[1])
        if n == 0 and m == 0:
            break
        
        # 读入迷宫
        g = []
        xs = ys = xe = ye = None
        snake_index = {}
        snake_count = 0
        for i in range(n):
            row = list(data[line_index].strip())
            line_index += 1
            for j, ch in enumerate(row):
                if ch == 'K':
                    xs, ys = i, j
                elif ch == 'T':
                    xe, ye = i, j
                elif ch == 'S':
                    snake_index[(i, j)] = snake_count
                    snake_count += 1
            g.append(row)
        
        # 预处理：BFS 判断目标和所有钥匙是否可达（忽略杀蛇额外时间）
        reachable = [[False]*n for _ in range(n)]
        # flag[0] 表示唐僧所在房间可达，flag[1..m] 表示钥匙1..m可达
        flag = [False]*(m+1)
        q = deque([(xs, ys)])
        reachable[xs][ys] = True
        while q:
            x0, y0 = q.popleft()
            for dx, dy in directions:
                x1, y1 = x0 + dx, y0 + dy
                if not (0 <= x1 < n and 0 <= y1 < n):
                    continue
                if g[x1][y1] == '#':
                    continue
                if not reachable[x1][y1]:
                    reachable[x1][y1] = True
                    q.append((x1, y1))
                    if g[x1][y1].isdigit():
                        key_val = int(g[x1][y1])
                        if 1 <= key_val <= m:
                            flag[key_val] = True
                    elif x1 == xe and y1 == ye:
                        flag[0] = True
        # 如果目标房间或任一必须钥匙不可达，直接输出 "impossible"
        if not (flag[0] and all(flag[1:])):
            results.append("impossible")
            continue
        
        # 若预处理通过，则利用 Dijkstra 求最短时间
        # 状态编码：将 (已取钥匙数, 蛇杀记) 合并为一个整数
        def encode(keys, smask):
            return keys * (1 << snake_count) + smask
        
        # 在每个格子上用字典记录状态编码对应的最短耗时，降低内存占用
        visited = [[{} for _ in range(n)] for _ in range(n)]
        init_state = encode(0, 0)
        visited[xs][ys][init_state] = 0
        heap = [(0, xs, ys, 0, 0)]  # (耗时, x, y, keys, snake_mask)
        ans = -1
        while heap:
            t, x, y, keys, smask = heapq.heappop(heap)
            state_code = encode(keys, smask)
            if visited[x][y].get(state_code, float('inf')) < t:
                continue
            if x == xe and y == ye and keys == m:
                ans = t
                break
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < n and 0 <= ny < n):
                    continue
                if g[nx][ny] == '#':
                    continue
                nkeys = keys
                nsmask = smask
                nt = t + 1  # 每走一步耗时1分钟
                cell = g[nx][ny]
                # 若该房间有蛇且尚未杀死，则需额外1分钟，并更新蛇状态
                if cell == 'S':
                    idx = snake_index[(nx, ny)]
                    if not (smask & (1 << idx)):
                        nt += 1
                        nsmask = smask | (1 << idx)
                # 若该房间有钥匙且正是下一个需要的钥匙，则拾取钥匙
                if cell.isdigit():
                    k = int(cell)
                    if keys < m and k == keys + 1:
                        nkeys = keys + 1
                new_state = encode(nkeys, nsmask)
                if new_state not in visited[nx][ny] or nt < visited[nx][ny][new_state]:
                    visited[nx][ny][new_state] = nt
                    heapq.heappush(heap, (nt, nx, ny, nkeys, nsmask))
        results.append("impossible" if ans == -1 else str(ans))
    
    sys.stdout.write("\n".join(results))
    
if __name__ == '__main__':
    solve()
