# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2774: 木材加工
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02774/
# License: not declared in source collection; no license is inferred.
import sys
n, k = map(int, input().split())
expenditure = []
for _ in range(n):
    expenditure.append(int(input()))


def check(x):
    num = 0
    for i in range(n):
        num += expenditure[i] // x

    return num >= k

lo = 1
hi = max(expenditure) + 1

if sum(expenditure) < k:
    print(0)
    exit()

ans = 1
while lo < hi:
    mid = (lo + hi) // 2
    if check(mid):
        ans = mid
        lo = mid + 1
    else:
        hi = mid

print(ans)
