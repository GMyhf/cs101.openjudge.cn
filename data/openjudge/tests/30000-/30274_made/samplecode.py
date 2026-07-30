# External reference: http://cs101.openjudge.cn/practice/30274/statistics/
# Accepted submission: 52194862
# Source: http://cs101.openjudge.cn/practice/solution/52194862/
# License: not declared on the submission page; no license is inferred.

global m
n,m=[int(i) for i in input().split()]
l=[int(i) for i in input().split()]

def operation(x,y):
    if x+y>=m:
        return 0
    else:
        return x+y
def calculate(x,y):
    total=set()
    for i in x:
        for j in y:
            total.update([operation(i,j)])
    return total


#dp[(i,j)]表示下标区间[i,j]上的最大值结果，其中0<=i<=j<=n-1
dp={}
for i in range(n):
    for j in range(i,n):
        dp[(i,j)]=set()

for i in range(n):
    dp[(i,i)].add(operation(l[i],0))

for dev in range(1,n):
    for ptr1 in range(0,n-dev):
        ptr2=ptr1+dev
        for k in range(ptr1,ptr2):
            dp[(ptr1,ptr2)].update(calculate(dp[(ptr1,k)],dp[(k+1,ptr2)]))


print(max(dp[(0,n-1)]))
