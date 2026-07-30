# External reference: http://cs101.openjudge.cn/practice/26971/statistics/
# Accepted submission: 52498222
# Source: http://cs101.openjudge.cn/practice/solution/52498222/
# License: not declared on the submission page; no license is inferred.

n=int(input())
ratings=[int(i) for i in input().split()]
past=ratings[0]
left=[0]*n
past=ratings[0]
left[0]=1
for i in range(1,n):
    if ratings[i]>past:
        left[i]=left[i-1]+1
    else:
        left[i]=1
    past=ratings[i]
right=[0]*n
past=ratings[-1]
right[-1]=1
for i in range(n-2,-1,-1):
    if ratings[i]>past:
        right[i]=right[i+1]+1
    else:
        right[i]=1
    past=ratings[i]
result=sum(max(left[i],right[i]) for i in range(n))
print(result)
