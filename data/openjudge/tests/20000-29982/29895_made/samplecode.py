# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import math

n = int(input())
for i in range(2, int(math.isqrt(n)) + 1):
    if n % i == 0:
        print(n // i)
        break
