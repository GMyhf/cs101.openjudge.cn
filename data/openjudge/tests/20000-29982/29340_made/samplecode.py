# External reference: statistics page /practice/29340/
# Accepted submission: 52734019
# Source: http://cs101.openjudge.cn/practice/solution/52734019/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法枚举左端点再向右扩展，最坏 O(n^2)，n=10^4 且答案很长或为 -1 时超时。
# 新写法：区间变长极差不减，故右端点右移时最优左端点也只右移；双指针 + 单调队列维护窗口最大/最小值，O(n)。
import sys
from collections import deque

data = sys.stdin.read().split()
n = int(data[0])
nums = list(map(int, data[1:n + 1]))
k = int(data[n + 1])

min_len = float('inf')
max_q = deque()  # 窗口内下标，对应值单调递减，队首是最大值
min_q = deque()  # 窗口内下标，对应值单调递增，队首是最小值
left = 0

# 枚举所有右端点
for j in range(n):
    x = nums[j]
    while max_q and nums[max_q[-1]] <= x:
        max_q.pop()
    while min_q and nums[min_q[-1]] >= x:
        min_q.pop()
    max_q.append(j)
    min_q.append(j)
    # 窗口 [left, j] 满足条件就记录长度，并尝试收缩左端点
    while left <= j and nums[max_q[0]] - nums[min_q[0]] >= k:
        min_len = min(min_len, j - left + 1)
        left += 1
        if max_q[0] < left:
            max_q.popleft()
        if min_q[0] < left:
            min_q.popleft()

if min_len != float('inf'):
    print(min_len)
else:
    print(-1)
