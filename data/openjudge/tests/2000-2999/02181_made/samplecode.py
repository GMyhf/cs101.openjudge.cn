# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2181: Jumping Cows
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02181/
# License: not declared; no license is inferred.
import sys
# 2300010763	胡睿诚	数学科学学院
P = int(input())
potions = []
for i in range(P):
    potions.append((int(input())))
result = 0
sign = 1
for i in range(P-1):
    if (potions[i + 1] - potions[i]) * sign < 0:
        result += sign * potions[i]
        sign = -sign
if sign == 1:
    result += potions[P-1]
print(result)
