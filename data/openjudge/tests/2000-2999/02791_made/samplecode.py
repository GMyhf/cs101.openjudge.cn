# External reference: statistics page /practice/02791/
# Accepted submission: 49065965
# Source: http://cs101.openjudge.cn/practice/solution/49065965/
# License: not declared on the submission page; no license is inferred.

import sys

def main():
    while True:
        n = int(sys.stdin.readline())
        if n == 0:
            break
        points = []
        for _ in range(n):
            x, y = map(int, sys.stdin.readline().split())
            points.append((x, y))

        candidates = []
        visited = set()

        # 枚举所有子集，大小至少为2
        for mask in range(1, 1 << n):
            bit_count = bin(mask).count('1')
            if bit_count < 2:
                continue

            tx = []
            ty = []
            for i in range(n):
                if mask & (1 << i):
                    tx.append(points[i][0])
                    ty.append(points[i][1])

            min_x, max_x = min(tx), max(tx)
            if max_x == min_x:
                left, right = min_x, min_x + 1
            else:
                left, right = min_x, max_x

            min_y, max_y = min(ty), max(ty)
            if max_y == min_y:
                bottom, top = min_y, min_y + 1
            else:
                bottom, top = min_y, max_y

            cover_mask = 0
            for i in range(n):
                x, y = points[i]
                if left <= x <= right and bottom <= y <= top:
                    cover_mask |= (1 << i)

            key = (left, right, bottom, top)
            if key not in visited:
                visited.add(key)
                area = (right - left) * (top - bottom)
                candidates.append((cover_mask, area))

        INF = float('inf')
        dp = [INF] * (1 << n)
        dp[0] = 0

        for mask in range(1 << n):
            if dp[mask] == INF:
                continue
            for cover_mask, area in candidates:
                new_mask = mask | cover_mask
                if dp[new_mask] > dp[mask] + area:
                    dp[new_mask] = dp[mask] + area

        print(dp[(1 << n) - 1])

if __name__ == '__main__':
    main()
