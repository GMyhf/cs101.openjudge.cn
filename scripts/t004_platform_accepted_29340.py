# External reference: statistics page /practice/29340/
# Accepted submission: 52734019
# Source: http://cs101.openjudge.cn/practice/solution/52734019/
# License: not declared on the submission page; no license is inferred.

n = int(input())
nums = list(map(int, input().split()))
k = int(input())

min_len = float('inf')

# 枚举所有左端点
for i in range(n):
    current_max = nums[i]
    current_min = nums[i]
    # 枚举所有右端点
    for j in range(i, n):
        current_max = max(current_max, nums[j])
        current_min = min(current_min, nums[j])
        if current_max - current_min >= k:
            min_len = min(min_len, j - i + 1)
            break  # 更短不可能，直接跳出

if min_len != float('inf'):
    print(min_len)
else:
    print(-1)