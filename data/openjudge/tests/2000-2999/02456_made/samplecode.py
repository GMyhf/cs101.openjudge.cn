# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2456: Aggressive cows
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02456/
# License: not declared in source collection; no license is inferred.
import sys
from typing import List

class Solution:
    def maxDistance(self, stalls: List[int], cows: int) -> int:
        stalls.sort()

        def can_place(distance: int) -> bool:
            count = 1  # 第一个牛放在第一个stall
            last_pos = stalls[0]
            for pos in stalls[1:]:
                if pos - last_pos >= distance:
                    count += 1
                    last_pos = pos
                    if count >= cows:
                        return True
            return False

        left, right = 1, stalls[-1] - stalls[0] + 1  # 开区间写法
        ans = 0
        while left < right:
            mid = (left + right) // 2
            if can_place(mid):
                ans = mid
                left = mid + 1  # 能放，尝试更大
            else:
                right = mid  # 不能放，缩小范围
        return ans


# 用法示例
if __name__ == "__main__":
    N, C = map(int, input().split())
    stalls = [int(input()) for _ in range(N)]
    sol = Solution()
    print(sol.maxDistance(stalls, C))
