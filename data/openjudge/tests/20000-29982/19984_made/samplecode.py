# External reference: statistics page /practice/19984/
# Accepted submission: 22475453
# Source: http://cs101.openjudge.cn/practice/solution/22475453/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19984 statistics, Accepted solution 22475453.
# Source: http://cs101.openjudge.cn/practice/solution/22475453/
# Statistics: http://cs101.openjudge.cn/practice/19984/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
f=[-1]*(n+1)
p=[]
f[0]=float(input())
for i in range(n):
    p.append(tuple(map(float,input().split())))
f[1]=(2*f[0]+100)/p[0][0]
b=[0]*n
for i in range(1,n):
    for j in range(i+1):
        if p[i][j]==0:
            continue
        if f[i+1]==-1:
            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]
            b[i]=j
        elif f[i+1]>(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]:
            f[i+1]=(f[i]+f[j]+100-(1-p[i][j])*f[i-1])/p[i][j]
            b[i]=j
print(' '.join(map(str,b)))
print("%.2f" % f[n])
