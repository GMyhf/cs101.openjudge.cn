# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from collections import defaultdict
n,m1,m2=map(int,input().split())
d=defaultdict(int)
l1,l2=[],[]
for i in range(m1):
    l1.append(tuple(map(int,input().split())))
for i in range(m2):
    l2.append(tuple(map(int,input().split())))
for i in range(m1):
    for j in range(m2):
        if l1[i][1]==l2[j][0]:
            d[(l1[i][0],l2[j][1])]+=l1[i][2]*l2[j][2]
for i in range(n):
    for j in range(n):
        if d[(i,j)]:
            print(i,j,d[(i,j)])
