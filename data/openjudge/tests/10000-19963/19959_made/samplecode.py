# External reference: http://cs101.openjudge.cn/practice/19959/statistics/
# Accepted submission: 51286744
# Source: http://cs101.openjudge.cn/practice/solution/51286744/
# License: not declared on the submission page; no license is inferred.

n = int(input().strip())
ans = 0
i = 1
while i <= n:
    q = n // i
    j = n // q
    cnt = j - i + 1
    sum_k = (i + j) * cnt // 2
    block_sum = sum_k * (q * (q + 1) // 2)
    ans += block_sum
    i = j + 1
print(ans)
