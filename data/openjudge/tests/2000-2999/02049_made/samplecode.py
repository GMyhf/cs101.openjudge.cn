# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2049: Finding Nemo
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02049/
# License: not declared; no license is inferred.
# 本地修订：原代码用普通 BFS（入队即标记访问）累计门数，求的是“步数最短路径上的门数”，
# 不是最少门数；改为 0-1 BFS（不过门代价 0、过门代价 1）。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    p = 0
    out = []
    while True:
        m, n = int(data[p]), int(data[p + 1]); p += 2
        if m == -1 and n == -1:
            break
        # vert[x][y]: 竖直单位段 (x,y)-(x,y+1)；horz[x][y]: 水平单位段 (x,y)-(x+1,y)；0 空 1 墙 2 门
        vert = [[0] * 201 for _ in range(201)]
        horz = [[0] * 201 for _ in range(201)]
        for _ in range(m):
            x, y, d, t = map(int, data[p:p + 4]); p += 4
            for k in range(t):
                if d:
                    vert[x][y + k] = 1
                else:
                    horz[x + k][y] = 1
        for _ in range(n):
            x, y, d = map(int, data[p:p + 3]); p += 3
            if d:
                vert[x][y] = 2
            else:
                horz[x][y] = 2
        fx, fy = float(data[p]), float(data[p + 1]); p += 2
        sx, sy = int(fx), int(fy)
        # 格子 (i,j) 表示 [i,i+1]x[j,j+1]；i 或 j 为 0 或 >=199 的格子在所有墙之外，与 (0,0) 连通
        if sx <= 0 or sy <= 0 or sx >= 199 or sy >= 199:
            out.append(0)
            continue
        INF = 1 << 30
        dist = [[INF] * 200 for _ in range(200)]
        dist[sx][sy] = 0
        dq = deque([(sx, sy)])
        ans = -1
        while dq:
            i, j = dq.popleft()
            d0 = dist[i][j]
            if i == 0 or j == 0 or i == 199 or j == 199:
                ans = d0
                break
            for ni, nj, st in ((i + 1, j, vert[i + 1][j]), (i - 1, j, vert[i][j]),
                               (i, j + 1, horz[i][j + 1]), (i, j - 1, horz[i][j])):
                if st == 1:
                    continue
                c = 1 if st == 2 else 0
                if d0 + c < dist[ni][nj]:
                    dist[ni][nj] = d0 + c
                    if c:
                        dq.append((ni, nj))
                    else:
                        dq.appendleft((ni, nj))
        out.append(ans)
    print("\n".join(map(str, out)))

main()
