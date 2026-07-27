# External reference: cs101.openjudge.cn practice/20103 statistics, Accepted solution 43490046.
# Source: http://cs101.openjudge.cn/practice/solution/43490046/
# Statistics: http://cs101.openjudge.cn/practice/20103/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
m,l=[-float("inf")],[0]
for i in range(n):
    mi,li=map(int,input().split())
    m.append(mi)
    l.append(li)
m.append(float("inf"))
l.append(0)
ans=0
end=-float("inf")
for i in range(1,n+1):
    if m[i-1]<m[i]-l[i] and end<m[i]-l[i] and  m[i]+l[i]<m[i+1]:
        ans+=1
        end=m[i]+l[i]
print(ans)
