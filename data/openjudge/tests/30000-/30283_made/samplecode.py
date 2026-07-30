# External reference: http://cs101.openjudge.cn/practice/30283/statistics/
# Accepted submission: 52740187
# Source: http://cs101.openjudge.cn/practice/solution/52740187/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

# 骑士的 8 个日字走法
dx = [1, 1, -1, -1, 2, 2, -2, -2]
dy = [2, -2, 2, -2, 1, -1, 1, -1]

def bfs(start, end):
    sx, sy = start
    ex, ey = end
    if sx == ex and sy == ey:
        return 0

    # 双向 BFS 初始化
    q1 = deque()
    q2 = deque()
    vis1 = [[-1] * 1000 for _ in range(1000)]
    vis2 = [[-1] * 1000 for _ in range(1000)]

    q1.append((sx, sy))
    q2.append((ex, ey))
    vis1[sx][sy] = 0
    vis2[ex][ey] = 0

    while q1 and q2:
        # 扩展正向队列
        size = len(q1)
        for _ in range(size):
            x, y = q1.popleft()
            for i in range(8):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < 1000 and 0 <= ny < 1000:
                    if vis1[nx][ny] == -1:
                        vis1[nx][ny] = vis1[x][y] + 1
                        if vis2[nx][ny] != -1:
                            return vis1[nx][ny] + vis2[nx][ny]
                        q1.append((nx, ny))

        # 扩展反向队列
        size = len(q2)
        for _ in range(size):
            x, y = q2.popleft()
            for i in range(8):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 <= nx < 1000 and 0 <= ny < 1000:
                    if vis2[nx][ny] == -1:
                        vis2[nx][ny] = vis2[x][y] + 1
                        if vis1[nx][ny] != -1:
                            return vis1[nx][ny] + vis2[nx][ny]
                        q2.append((nx, ny))
    return -1

def main():
    input = sys.stdin.read
    data = input().split()
    t = int(data[0])
    idx = 1
    for _ in range(t):
        x1 = int(data[idx])
        y1 = int(data[idx+1])
        x2 = int(data[idx+2])
        y2 = int(data[idx+3])
        idx +=4
        print(bfs((x1,y1), (x2,y2)))

if __name__ == "__main__":
    main()
