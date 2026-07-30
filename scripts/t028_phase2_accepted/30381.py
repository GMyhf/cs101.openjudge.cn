# External reference: http://cs101.openjudge.cn/practice/30381/statistics/
# Accepted submission: 52723494
# Source: http://cs101.openjudge.cn/practice/solution/52723494/
# License: not declared on the submission page; no license is inferred.

# 读取输入
N, M = map(int, input().split())
c = list(map(int, input().split()))

# 二分查找左右边界
left = 0
# 右边界设为最大卡片数 + 万能卡数（理论最大值）
right = max(c) + M
ans = 0

while left <= right:
    mid = (left + right) // 2
    need = 0
    for num in c:
        if num < mid:
            need += mid - num
    # 核心判断条件
    if need <= M and need <= mid:
        ans = mid
        left = mid + 1  # 尝试更大的套数
    else:
        right = mid - 1  # 套数太大，缩小范围

print(ans)
