# External reference: http://cs101.openjudge.cn/practice/01324/statistics/
# Accepted submission: 43827108
# Source: http://cs101.openjudge.cn/practice/solution/43827108/
# License: not declared on the submission page; no license is inferred.

# https://www.cnblogs.com/wiklvrain/p/8179443.html
from collections import deque

# Constants for the maximum grid size
maxn = 21
# Directions representing right, down, left, up
dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]


# Function to judge if a move is valid
def judge(p, t, l):
    a, b = p[0], p[1]
    row, col = a + dir[t][0], b + dir[t][1]
    if row == a and col == b:
        return False
    k = l - 1
    while k:
        q = p[2] & 3
        p = (p[0], p[1], p[2] >> 2)
        nx, ny = a + dir[q][0], b + dir[q][1]
        if nx == row and ny == col:
            return False
        a, b = nx, ny
        k -= 1
    return True


# BFS function to find the shortest path for the snake
def bfs(s, n, m, l, g):
    q = deque()
    vis = [[[0] * (1 << 14) for _ in range(maxn)] for _ in range(maxn)]

    q.append(s)
    vis[s[0]][s[1]][s[2]] = 1

    while q:
        p = q.popleft()
        if p[0] == 1 and p[1] == 1:
            return vis[p[0]][p[1]][p[2]] - 1
        for i in range(4):
            nx, ny = p[0] + dir[i][0], p[1] + dir[i][1]
            st = (p[2] & ((1 << (2 * (l - 2))) - 1)) << 2
            st |= (i + 2) % 4
            if 1 <= nx <= n and 1 <= ny <= m and not vis[nx][ny][st] and not g[nx][ny] and judge(p, i, l):
                vis[nx][ny][st] = vis[p[0]][p[1]][p[2]] + 1
                q.append((nx, ny, st))
    return -1


def main():
    cas = 1
    while True:
        n, m, l = map(int, input().split())
        if n == 0 and m == 0 and l == 0:
            break

        # Initialize the snake
        ss = (0, 0, 0)
        tmp1, tmp2 = 0, 0
        for i in range(l):
            a, b = map(int, input().split())
            if i == 0:
                ss = (a, b, 0)
            else:
                for j in range(4):
                    nx = tmp1 + dir[j][0]
                    ny = tmp2 + dir[j][1]
                    if nx == a and ny == b:
                        ss = (ss[0], ss[1], ss[2] | (j << (2 * (i - 1))))
                        break
            tmp1, tmp2 = a, b

        # Read obstacles
        k = int(input())
        g = [[0] * maxn for _ in range(maxn)]
        #for _ in range(k):
        while k:
            try:
                a, b = map(int, input().split())
            except ValueError:
                continue
            k -= 1

            g[a][b] = 1

        # Perform BFS
        result = bfs(ss, n, m, l, g)
        print(f"Case {cas}: {result}")
        cas += 1
        input()


if __name__ == "__main__":
    main()
