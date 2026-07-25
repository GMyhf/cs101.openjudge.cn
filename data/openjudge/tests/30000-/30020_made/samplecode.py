# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from math import ceil
def fill(vacancy,goods):
    filled = min(vacancy,goods)
    vacancy -= filled
    goods -= filled
    return vacancy,goods

a,b,c,d,e = map(int,input().split())
total = 0

# carriers for pizza
total += a
vacancy,d = fill(a*5,d) #1*2 fit in space_11
vacancy,e = fill(vacancy*2+a,e) # 1*1 fit in space 1

# carriers for steak
total += (b+1)//2
vacancy = (b+1)//2*6 - b*2
vacancy,c = fill(vacancy,c)
vacancy,d = fill(vacancy*3,d)
vacancy,e = fill(vacancy*2,e)

# carriers for the remainder
total += ceil((6*c+2*d+1*e)/36)

print(total)
