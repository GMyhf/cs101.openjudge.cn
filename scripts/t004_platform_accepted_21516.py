# External reference: statistics page /practice/21516/
# Accepted submission: 47436368
# Source: http://cs101.openjudge.cn/practice/solution/47436368/
# License: not declared on the submission page; no license is inferred.

a,b=map(int,input().split());c={i:[]for i in range(a+1)};f={i:0 for i in c};import sys;sys.setrecursionlimit(1<<30)
for i in range(b):d,e=map(int,input().split());c[d].append(e)
def r(z):
    global f
    if f[z]:x={p,f[z]};return x
    else:f[z]=p;x={p}
    for k in c[z]:x|=r(k)
    return x
def s(z):global f;a=z if z==f[z]else s(f[z]);f[z]=a;return a
for i in c:
    if 1<len(c[i])and f[i]==0:
        g=set();p=min(c[i])
        for j in c[i]:g|=r(j)
        h=min(s(z)for z in g)
        for j in g:f[j]=h
k={i:0 for i in c};g=0
for i in c:
    if f[i]:k[s(i)]+=1
    else:g+=len(c[i])
print(g+sum((k[i]-1)*k[i]for i in k))