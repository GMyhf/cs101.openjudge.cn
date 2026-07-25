# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import math
t = int(input())
for _ in range(t):
    n = int(input())
    if n % 2 == 1:
        sumv = (1 + n - 1)*(n-1)//2 + n
    else:
        sumv = (1 + n)*n//2
    
    maxp = int(math.log2(n))
    
    for i in range(maxp+1):
        sumv -= 2*(2**i)
    
    print(sumv)
