# External reference: http://cs101.openjudge.cn/practice/29949/statistics/
# Accepted submission: 52491340
# Source: http://cs101.openjudge.cn/practice/solution/52491340/
# License: not declared on the submission page; no license is inferred.

n,m=[int(i) for i in input().split()]
stones=[]
for _ in range(n):
    v,w=[int(i) for i in input().split()]
    stones.append((v,w))
stones.sort(reverse=True,key=lambda x:x[0]/x[1])
value=0
space=m
for val,weight in stones:
    if space>=weight:
        space-=weight
        value+=val
    elif space==0:
        break
    else:
        value+=space*(val/weight)
        space=0
        break
print(format(value,".2f"))
