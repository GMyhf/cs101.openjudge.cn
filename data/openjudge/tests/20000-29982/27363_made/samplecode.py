# External reference: http://cs101.openjudge.cn/practice/27363/statistics/
# Accepted submission: 52506041
# Source: http://cs101.openjudge.cn/practice/solution/52506041/
# License: not declared on the submission page; no license is inferred.

import sys

input_data = sys.stdin.read().split()
if not input_data:
    exit()
I = iter(input_data)
n = int(next(I))

# 修复 2：初始化为 -1，因为 0 是合法的数组下标
start = [-1] * (n + 1)
end = [-1] * (n + 1)

nums = [int(next(I)) for _ in range(n)]

# 预处理起点和终点
for j, num in enumerate(nums):
    if num == 0:
        continue
    if start[num] == -1:
        start[num] = j
    end[num] = j

stack = []
ans = 0

for j, num in enumerate(nums):
    if num == 0:
        if stack:
            print(-1)
            ans = -1
            break
        continue

    # 修复 1：独立的 if，保证 start == end 时能先入栈
    if j == start[num]:
        stack.append(num)
        # 修复 3：答案应该是栈的历史最大深度
        ans = max(ans, len(stack))

    # 修复 1：不能用 elif，必须是独立的 if
    if j == end[num]:
        if stack[-1] != num:
            print(-1)
            ans = -1
            break
        stack.pop()

if ans != -1:
    print(ans)
