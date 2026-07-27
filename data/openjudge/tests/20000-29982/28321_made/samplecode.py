# External reference: statistics page /practice/28321/
# Accepted submission: 52459418
# Source: http://cs101.openjudge.cn/practice/solution/52459418/
# License: not declared on the submission page; no license is inferred.

t = int(input())
for l in range(t):
    n = int(input())
    a = list(map(int,input().split()))
    b = list(map(int,input().split()))
    ans = 0
    j = 0
    for i,num in enumerate(b):
        while j < n and a[j] < b[i]:
            j += 1
        ans = max(ans,max(j-i,0))
        if j == n-1:
            break
    print(ans)
