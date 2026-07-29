# External reference: http://cs101.openjudge.cn/practice/02251/statistics/
# Accepted submission: 52718463
# Source: http://cs101.openjudge.cn/practice/solution/52718463/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 一次性读取所有输入，防止复杂的空白行处理问题
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    while True:
        try:
            L = int(next(iterator))
            R = int(next(iterator))
            C = int(next(iterator))
        except StopIteration:
            break

        # 输入以 0 0 0 结束
        if L == 0 and R == 0 and C == 0:
            break

        grid = []
        start = None
        end = None

        # 构建三维地图并记录起点与终点
        for l in range(L):
            level = []
            for r in range(R):
                row_str = next(iterator)
                row = list(row_str)
                level.append(row)
                for c in range(C):
                    if row[c] == 'S':
                        start = (l, r, c)
                    elif row[c] == 'E':
                        end = (l, r, c)
            grid.append(level)

        if not start or not end:
            print("Trapped!")
            continue

        sl, sr, sc = start
        queue = deque([(sl, sr, sc, 0)])
        grid[sl][sr][sc] = '#'  # 标记起点为已访问

        escaped = False
        # 6个移动方向：上下、南北、东西
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]

        while queue:
            l, r, c, dist = queue.popleft()

            # 如果到达终点
            if (l, r, c) == end:
                print(f"Escaped in {dist} minute(s).")
                escaped = True
                break

            for dl, dr, dc in directions:
                nl, nr, nc = l + dl, r + dr, c + dc
                # 检查边界条件
                if 0 <= nl < L and 0 <= nr < R and 0 <= nc < C:
                    # 如果是可行走区域或出口
                    if grid[nl][nr][nc] == '.' or grid[nl][nr][nc] == 'E':
                        # 如果是出口，可以提前判断并退出
                        if grid[nl][nr][nc] == 'E':
                            print(f"Escaped in {dist + 1} minute(s).")
                            escaped = True
                            queue.clear() # 清空队列以退出外层循环
                            break
                        # 标记为已访问，避免重复入队
                        grid[nl][nr][nc] = '#'
                        queue.append((nl, nr, nc, dist + 1))
            if escaped:
                break

        if not escaped:
            print("Trapped!")

if __name__ == '__main__':
    solve()
