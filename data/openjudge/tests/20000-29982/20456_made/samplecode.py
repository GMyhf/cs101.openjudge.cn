# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def closedIsland(grid):
    rows, cols = len(grid), len(grid[0])

    # 检查岛屿是否封闭的DFS函数
    def dfs(r, c):
        if grid[r][c] == 1:
            return True
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return False
        
        # 标记当前单元格为已访问
        grid[r][c] = 1
        
        # 检查所有方向
        up = dfs(r - 1, c)
        down = dfs(r + 1, c)
        left = dfs(r, c - 1)
        right = dfs(r, c + 1)
        
        return up and down and left and right

    closed_islands = 0
    for r in range(1, rows - 1):  # 从1开始，忽略边界
        for c in range(1, cols - 1):  # 从1开始，忽略边界
            if grid[r][c] == 0 and dfs(r, c):
                closed_islands += 1

    return closed_islands

# 读取输入
grid = []
for _ in range(10):
    row = list(map(int, input().split(',')))
    grid.append(row)

# 输出结果
print(closedIsland(grid))

