import random
import time
import os
import sys
from collections import deque
import copy

# 增加递归深度，防止 DFS 爆栈
sys.setrecursionlimit(10**6)

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

# ----------------------------------------------------------------------------
# AC 代码逻辑封装
# ----------------------------------------------------------------------------
def solve_ac(n, original_maze):
    # 深拷贝地图，因为 AC 代码会修改地图内容 (将 1 改为 2)
    maze = [row[:] for row in original_maze]
    
    move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    q = deque()

    def tong(x, y, q, maze):
        """DFS标记第一个岛屿，并将边界点加入队列"""
        maze[x][y] = '2'
        q.append((x, y))
        for dx, dy in move:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and maze[nx][ny] == '1':
                tong(nx, ny, q, maze)

    def bfs(q, maze):
        """BFS寻找第二个岛屿的最短距离"""
        s = 0
        while q:
            for _ in range(len(q)):
                x, y = q.popleft()
                for dx, dy in move:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        if maze[nx][ny] == '1':  # 找到第二个岛屿
                            return s
                        if maze[nx][ny] == '0':  # 水域，加入队列
                            maze[nx][ny] = '2'  # 标记为访问过
                            q.append((nx, ny))
            s += 1
        return s

    found = False
    result = 0
    
    for i in range(n):
        if found:
            break
        for j in range(n):
            if maze[i][j] == '1':  # 找到第一个岛屿
                tong(i, j, q, maze)
                result = bfs(q, maze)
                found = True
                break
    return result

# ----------------------------------------------------------------------------
# 数据生成逻辑
# ----------------------------------------------------------------------------
def check_validity(n, maze):
    """
    检查地图是否合法：必须恰好有2个连通分量（2个孤岛）。
    使用并查集或BFS/DFS计数。
    """
    visited = [[False] * n for _ in range(n)]
    islands_count = 0
    move = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(n):
        for c in range(n):
            if maze[r][c] == '1' and not visited[r][c]:
                islands_count += 1
                if islands_count > 2: return False # 太多岛
                
                # BFS 遍历整个当前岛屿
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    for dr, dc in move:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == '1' and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
    
    return islands_count == 2

def generate_map(n):
    """生成一个 nxn 的地图，保证恰好有两个孤岛"""
    while True:
        # 1. 初始化全水域
        grid = [['0'] * n for _ in range(n)]
        
        # 2. 随机生成两个种子点 (保证距离不贴在一起)
        p1 = (random.randint(0, n-1), random.randint(0, n-1))
        p2 = (random.randint(0, n-1), random.randint(0, n-1))
        
        # 简单的曼哈顿距离检查，避免种子太近
        if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) < 3:
            continue

        # 3. 生长岛屿
        # 参数：每个岛屿生长的步数。步数越多岛越大。
        # 随机步数，大约占地图面积的一小部分，避免填满
        max_steps = max(1, (n * n) // 6) 
        
        seeds = [p1, p2]
        
        for seed in seeds:
            grid[seed[0]][seed[1]] = '1'
            curr_x, curr_y = seed
            steps = random.randint(1, max_steps)
            
            for _ in range(steps):
                # 随机游走
                dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                dx, dy = random.choice(dirs)
                nx, ny = curr_x + dx, curr_y + dy
                
                if 0 <= nx < n and 0 <= ny < n:
                    grid[nx][ny] = '1'
                    curr_x, curr_y = nx, ny # 移动当前笔触
                else:
                    # 如果出界，就重置回种子点或者保持原地
                    curr_x, curr_y = seed
        
        # 4. 验证是否合法 (恰好2个岛，且不相连)
        if check_validity(n, grid):
            return grid
        
        # 如果不合法（比如两个岛长到一起去了，或者某次随机没长出来），循环重试

# ----------------------------------------------------------------------------
# 主程序
# ----------------------------------------------------------------------------

for epoch in range(20):
    # 随机生成 n
    # 前5个测试点生成小图，方便调试观察
    if epoch < 5:
        n = random.randint(4, 8)
    # 中间生成中等图
    elif epoch < 15:
        n = random.randint(10, 30)
    # 最后生成大图 (根据题目难度，通常 N <= 100)
    else:
        n = random.randint(40, 100)

    # 生成地图数据
    maze_grid = generate_map(n)
    
    # 构造输入字符串
    input_lines = [str(n)]
    for row in maze_grid:
        input_lines.append("".join(row))
    input_str = "\n".join(input_lines) + "\n"

    # 写入输入文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(input_str)

    start = time.time()

    # 调用 AC 逻辑求解
    # 注意：generate_map 返回的是字符列表的列表，ac代码需要 list(input()) 格式
    # 这里我们直接传 maze_grid 即可，因为它的结构就是 [['1','0',...], ...]
    ans = solve_ac(n, maze_grid)

    end = time.time() - start
    print(f"[{epoch}] {end:.3f}s | n={n}, ans={ans}")

    # 写入输出文件
    with open(f"data/{epoch}.out", "w") as f:
        f.write(str(ans) + "\n")
