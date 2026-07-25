# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from functools import lru_cache

def count_partitions(n, k):
    @lru_cache(maxsize=None)
    def dfs(n, k, start):
        if k == 1:
            return 1 if n >= start else 0

        count = 0
        for i in range(start, n + 1):
            count += dfs(n - i, k - 1, i)
        return count
    return dfs(n, k, 1)

n, k = map(int, input().split())
print(count_partitions(n, k))
