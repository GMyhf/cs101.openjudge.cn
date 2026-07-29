# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2748: 全排列
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/pctbook/02748/
# License: not declared in source collection; no license is inferred.
import sys
from typing import List

class Solution:
    def permute(self, s: str) -> List[str]:
        ans = []

        def back(remaining: str, path: str):
            if not remaining:
                ans.append(path)
                return
            for i in range(len(remaining)):
                back(remaining[:i] + remaining[i+1:], path + remaining[i])

        back(s, "")
        return ans


# 测试
s = input().strip()
solution = Solution()
for p in solution.permute(s):
    print(p)
