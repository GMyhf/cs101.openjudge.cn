# External reference: /practice/29945/statistics/
# Accepted submission: 52733426
# Source: http://cs101.openjudge.cn/practice/solution/52733426/
# License: not declared on the submission page; no license is inferred.

n = int(input())
while n != 1:
    if n % 2 == 1:
        nxt = n * 3 + 1
        print(f"{n}*3+1={nxt}")
    else:
        nxt = n // 2
        print(f"{n}/2={nxt}")
    n = nxt
print("End")