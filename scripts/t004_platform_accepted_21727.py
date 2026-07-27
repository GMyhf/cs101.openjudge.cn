# External reference: statistics page /practice/21727/
# Accepted submission: 51529747
# Source: http://cs101.openjudge.cn/practice/solution/51529747/
# License: not declared on the submission page; no license is inferred.

# 21727: 湾仔码头
# 贪心：优先装体积最小的砖

N, M = map(int, input().split())
bricks = list(map(int, input().split()))

total = 0
count = 0

for w in bricks:
    if total + w <= M:
        total += w
        count += 1
    else:
        break

print(count)
