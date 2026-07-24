# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        R, C, K = map(int, input().split())
        maze = [list(input().rstrip('\n')) for _ in range(R)]
        
        # Find S and E
        for i in range(R):
            for j in range(C):
                if maze[i][j] == 'S':
                    sr, sc = i, j
                elif maze[i][j] == 'E':
                    er, ec = i, j
        
        # dist[r][c][m] = minimum absolute time to reach (r,c) with time mod K == m
        INF = 10**18
        dist = [[[INF]*K for _ in range(C)] for __ in range(R)]
        
        dq = deque()
        dist[sr][sc][0] = 0
        dq.append((sr, sc, 0))  # at time 0
        
        ans = None
        while dq:
            r, c, m = dq.popleft()
            t = dist[r][c][m]
            # If we've reached the exit, record and break (BFS ensures minimal time)
            if (r, c) == (er, ec):
                ans = t
                break
            
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r+dr, c+dc
                nt = t + 1
                nm = nt % K
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                cell = maze[nr][nc]
                # If it's a rock, only allowed if nt % K == 0
                if cell == '#' and nm != 0:
                    continue
                # '.' or 'S' or 'E' always ok
                if dist[nr][nc][nm] > nt:
                    dist[nr][nc][nm] = nt
                    dq.append((nr, nc, nm))
        
        if ans is None:
            print("Oop!")
        else:
            print(ans)


if __name__ == "__main__":
    solve()
