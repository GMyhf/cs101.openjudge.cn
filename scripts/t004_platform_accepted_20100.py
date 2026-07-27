# External reference: cs101.openjudge.cn practice/20100 statistics, Accepted solution 43253417.
# Source: http://cs101.openjudge.cn/practice/solution/43253417/
# Statistics: http://cs101.openjudge.cn/practice/20100/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
v=list(map(int,input().split()))
r=list(map(int,input().split()))
t=list(map(int,input().split()))
vm=0
tm=1<<30
cnt=0
for i in range(n-1):
    v[i]/=t[i]
for i in range(n-1):
    if (v[i]>vm or t[i]<tm) and t[i]<r[i]:
        cnt+=1
    vm=max(vm,v[i])
    tm=min(tm,t[i])
print(cnt)
