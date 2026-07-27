# External reference: statistics page /practice/27421/
# Accepted submission: 52735753
# Source: http://cs101.openjudge.cn/practice/solution/52735753/
# License: not declared on the submission page; no license is inferred.

import heapq

def main():
    import sys
    input = sys.stdin.read().split()
    idx = 0
    m = int(input[idx])
    n = int(input[idx+1])
    idx +=2

    heightMap = []
    for i in range(m):
        row = list(map(int, input[idx:idx+n]))
        idx +=n
        heightMap.append(row)

    # 最小堆 + 访问矩阵
    heap = []
    visited = [[False]*n for _ in range(m)]

    # 放入四周边界
    for i in range(m):
        for j in range(n):
            if i==0 or i==m-1 or j==0 or j==n-1:
                heapq.heappush(heap, (heightMap[i][j], i, j))
                visited[i][j] = True

    # 四个方向
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    res = 0
    max_h = 0

    while heap:
        h, x, y = heapq.heappop(heap)
        max_h = max(max_h, h)

        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0<=nx<m and 0<=ny<n and not visited[nx][ny]:
                visited[nx][ny] = True
                if heightMap[nx][ny] < max_h:
                    res += max_h - heightMap[nx][ny]
                heapq.heappush(heap, (heightMap[nx][ny], nx, ny))

    print(res)

if __name__ == "__main__":
    main()