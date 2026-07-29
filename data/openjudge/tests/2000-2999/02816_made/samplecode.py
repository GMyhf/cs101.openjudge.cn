# External reference: http://cs101.openjudge.cn/practice/02816/statistics/
# Accepted submission: 52824847
# Source: http://cs101.openjudge.cn/practice/solution/52824847/
# License: not declared on the submission page; no license is inferred.

import sys


def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)

    while True:
        try:
            W_str = next(iterator)
            H_str = next(iterator)
        except StopIteration:
            break

        W = int(W_str)
        H = int(H_str)

        # 遇到 0 0 则输入结束
        if W == 0 and H == 0:
            break

        grid = []
        for _ in range(H):
            grid.append(list(next(iterator)))

        # 寻找起点 '@'
        start_y, start_x = -1, -1
        for y in range(H):
            for x in range(W):
                if grid[y][x] == "@":
                    start_y, start_x = y, x
                    break
            if start_y != -1:
                break

        # 使用 DFS 计算可到达的瓷砖数
        count = 0
        stack = [(start_y, start_x)]
        grid[start_y][start_x] = "#"  # 将起点标记为已访问，避免重复计算

        while stack:
            curr_y, curr_x = stack.pop()
            count += 1

            # 探索四个方向
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = curr_y + dy, curr_x + dx
                # 判断是否在网格边界内
                if 0 <= ny < H and 0 <= nx < W:
                    # 如果是黑色瓷砖，则标记并压入栈中
                    if grid[ny][nx] == ".":
                        grid[ny][nx] = "#"  # 标记为已访问
                        stack.append((ny, nx))

        print(count)


if __name__ == "__main__":
    solve()
