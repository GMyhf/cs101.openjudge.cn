# External reference: http://cs101.openjudge.cn/practice/28050/statistics/
# Accepted submission: 52726572
# Source: http://cs101.openjudge.cn/practice/solution/52726572/
# License: not declared on the submission page; no license is inferred.

from sys import setrecursionlimit
setrecursionlimit(1000000)

def solve_knight_tour(n, sr, sc):
    # 马的可能移动
    moves = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]

    board = [[-1]*n for _ in range(n)]  # -1 表示未访问
    board[sr][sc] = 0   # 第一步编号为 0

    # 预先计算每个格子的出度（下一步合法位置的数量），用于启发式排序
    def count_degree(x, y):
        cnt = 0
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
                cnt += 1
        return cnt

    # 对当前位置的合法邻居按下一步出度升序排序（Warnsdorff 规则）
    def get_sorted_neighbors(x, y):
        neighbors = []
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
                # 计算邻居的出度（不改变 board 状态）
                deg = count_degree(nx, ny)
                neighbors.append((deg, nx, ny))
        neighbors.sort()  # 按出度升序
        return [(nx, ny) for (_, nx, ny) in neighbors]

    # DFS 回溯
    def dfs(x, y, step):
        if step == n*n - 1:
            return True   # 所有格子都已走完

        for nx, ny in get_sorted_neighbors(x, y):
            board[nx][ny] = step + 1
            if dfs(nx, ny, step + 1):
                return True
            # 回溯
            board[nx][ny] = -1
        return False

    if dfs(sr, sc, 0):
        # 输出路径（每个格子被访问的顺序编号）
        print("success")
        # 如需输出坐标序列，可取消下一行的注释
        # for i in range(n):
        #     for j in range(n):
        #         print(f"{board[i][j]:3d}", end=" ")
        #     print()
    else:
        print("fail")

if __name__ == "__main__":
    n = int(input().strip())
    sr, sc = map(int, input().strip().split())
    solve_knight_tour(n, sr, sc)
