# External reference: statistics page /practice/04139/
# Accepted submission: 51213960
# Source: http://cs101.openjudge.cn/practice/solution/51213960/
# License: not declared on the submission page; no license is inferred.

a,b,c=map(int,input().split())
result=0
for k in range(c//b+1):
    if (c-b*k)%a==0:
        result+=1
print(result)