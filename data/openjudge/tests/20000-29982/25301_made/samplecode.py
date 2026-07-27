# External reference: statistics page /practice/25301/
# Accepted submission: 52328685
# Source: http://cs101.openjudge.cn/practice/solution/52328685/
# License: not declared on the submission page; no license is inferred.

n=int(input())
birs={}
for i in range(n):
    num,m,d=map(str,input().split())
    m,d=int(m),int(d)
    if (m,d) not in birs.keys():
        birs[(m,d)]=[num]
    else:
        birs[(m,d)].append(num)
days=list(birs.keys())
days.sort()
for m,d in days:
    if len(birs[(m,d)])>1:
        output=[m,d]
        for num in birs[(m,d)]:
            output.append(num)
        print(*output)