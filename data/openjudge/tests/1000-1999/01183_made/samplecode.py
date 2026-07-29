# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1183: 反正切函数的应用
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01183/
# License: not declared; no license is inferred.
import math
a=int(input())
m=a**2+1
for x in range(int(math.sqrt(m)),0,-1):
    if m%x==0:
        print(x+m//x+2*a)
        break
