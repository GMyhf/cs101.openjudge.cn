# External reference: http://cs101.openjudge.cn/practice/27104/statistics/
# Accepted submission: 52459416
# Source: http://cs101.openjudge.cn/practice/solution/52459416/
# License: not declared on the submission page; no license is inferred.

n=int(input())
a=[int(i) for i in input().split()]
site=[(i-a[i],i+a[i],i) for i in range(n)]
site.sort()
ptr=0
site_ptr=-1
cnt=0
current_right=-float('inf')
stack=[]
while ptr<n:
    while site_ptr+1<n and site[site_ptr+1][0]<=ptr:
        site_ptr+=1
        if stack:
            if site[site_ptr][1]>=stack[-1][1]:
                stack.append(site[site_ptr])
        else:
            stack.append(site[site_ptr])
    if ptr>current_right:
        current_right=stack[-1][1]
        cnt+=1
    ptr+=1
print(cnt)
