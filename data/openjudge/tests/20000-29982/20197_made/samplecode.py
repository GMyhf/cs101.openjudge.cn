# External reference: statistics page /practice/20197/
# Accepted submission: 52540070
# Source: http://cs101.openjudge.cn/practice/solution/52540070/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/20197/
# Accepted submission: 52540070
# Source: http://cs101.openjudge.cn/practice/solution/52540070/
# License: not declared on the submission page; no license is inferred.

n,m=map(int,input().split())
cnt=0
while m!=n:
    m,n=min(m,n),max(m,n)-min(m,n)
    cnt+=1
cnt+=1
print(cnt)