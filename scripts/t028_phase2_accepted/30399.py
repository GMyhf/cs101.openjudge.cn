# External reference: http://cs101.openjudge.cn/practice/30399/statistics/
# Accepted submission: 52723470
# Source: http://cs101.openjudge.cn/practice/solution/52723470/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    sys.setrecursionlimit(10000)
    m, n = map(int, sys.stdin.readline().split())
    heights = []
    for _ in range(m):
        row = list(map(int, sys.stdin.readline().split()))
        heights.append(row)

    # 方向：去太平洋只能 北、西
    dir_pac = [(-1, 0), (0, -1)]
    # 方向：去大西洋只能 南、东
    dir_atl = [(1, 0), (0, 1)]

    # DFS判断能否到达太平洋（北/西边界）
    def can_pac(r, c, visited):
        # 到达北/西边界，成功
        if r == 0 or c == 0:
            return True
        visited.add((r, c))
        for dr, dc in dir_pac:
            nr, nc = r + dr, c + dc
            # 越界/已访问/上坡，跳过
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and heights[nr][nc] <= heights[r][c]:
                if can_pac(nr, nc, visited):
                    return True
        return False

    # DFS判断能否到达大西洋（南/东边界）
    def can_atl(r, c, visited):
        # 到达南/东边界，成功
        if r == m-1 or c == n-1:
            return True
        visited.add((r, c))
        for dr, dc in dir_atl:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and heights[nr][nc] <= heights[r][c]:
                if can_atl(nr, nc, visited):
                    return True
        return False

    res = []
    # 按要求顺序遍历：从上到下，从左到右
    for r in range(m):
        for c in range(n):
            p = can_pac(r, c, set())
            a = can_atl(r, c, set())
            if p and a:
                res.append((r, c))

    # 输出结果
    if not res:
        print("None")
    else:
        for point in res:
            print(point[0], point[1])

if __name__ == "__main__":
    main()
