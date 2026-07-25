# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys
from functools import lru_cache

def can_player1_win(nums):
    n = len(nums)
    
    @lru_cache(maxsize=None)
    def diff(i, j):
        if i == j:
            return nums[i]
        return max(nums[i] - diff(i + 1, j), nums[j] - diff(i, j - 1))
    
    return diff(0, n - 1) >= 0

# 主程序读取输入
input = sys.stdin.read
data = input().split()

t = int(data[0])
index = 1
results = []

for _ in range(t):
    m = int(data[index])
    index += 1
    nums = list(map(int, data[index:index + m]))
    index += m
    results.append("true" if can_player1_win(nums) else "false")

# 输出结果
for res in results:
    print(res)
