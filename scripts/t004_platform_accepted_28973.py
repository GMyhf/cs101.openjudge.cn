# External reference: statistics page /practice/28973/
# Accepted submission: 52832149
# Source: http://cs101.openjudge.cn/practice/solution/52832149/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    grid = []
    idx = 1
    for _ in range(n):
        grid.append([int(x) for x in input_data[idx : idx + n]])
        idx += n
        
    # BFS 初始化
    # 队列中存储元素为 (r, c, d, steps)
    # d = 0 代表水平，d = 1 代表竖直
    queue = deque([(0, 0, 0, 0)])
    visited = [[[False] * 2 for _ in range(n)] for _ in range(n)]
    visited[0][0][0] = True
    
    target_r, target_c, target_d = n - 1, n - 2, 0
    
    while queue:
        r, c, d, steps = queue.popleft()
        
        # 到达目标状态
        if r == target_r and c == target_c and d == target_d:
            print(steps)
            return
            
        # 1. 向下移动
        if d == 0:
            if r + 1 < n and grid[r+1][c] == 0 and grid[r+1][c+1] == 0:
                if not visited[r+1][c][0]:
                    visited[r+1][c][0] = True
                    queue.append((r+1, c, 0, steps + 1))
        else: # d == 1
            if r + 2 < n and grid[r+2][c] == 0:
                if not visited[r+1][c][1]:
                    visited[r+1][c][1] = True
                    queue.append((r+1, c, 1, steps + 1))
                    
        # 2. 向右移动
        if d == 0:
            if c + 2 < n and grid[r][c+2] == 0:
                if not visited[r][c+1][0]:
                    visited[r][c+1][0] = True
                    queue.append((r, c+1, 0, steps + 1))
        else: # d == 1
            if c + 1 < n and grid[r][c+1] == 0 and grid[r+1][c+1] == 0:
                if not visited[r][c+1][1]:
                    visited[r][c+1][1] = True
                    queue.append((r, c+1, 1, steps + 1))
                    
        # 3. 旋转操作
        if d == 0:
            # 顺时针旋转，需要下方两个单元格为空
            if r + 1 < n and grid[r+1][c] == 0 and grid[r+1][c+1] == 0:
                if not visited[r][c][1]:
                    visited[r][c][1] = True
                    queue.append((r, c, 1, steps + 1))
        else: # d == 1
            # 逆时针旋转，需要右侧两个单元格为空
            if c + 1 < n and grid[r][c+1] == 0 and grid[r+1][c+1] == 0:
                if not visited[r][c][0]:
                    visited[r][c][0] = True
                    queue.append((r, c, 0, steps + 1))
                    
    # 无法到达目的地
    print(-1)

if __name__ == '__main__':
    solve()