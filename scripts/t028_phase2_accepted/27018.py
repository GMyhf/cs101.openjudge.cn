# External reference: http://cs101.openjudge.cn/practice/27018/statistics/
# Accepted submission: 52670403
# Source: http://cs101.openjudge.cn/practice/solution/52670403/
# License: not declared on the submission page; no license is inferred.

mod=998244353
N=int(input())
perm=list(map(int,input().split()))
fact=[1]*(N+1)
for i in range(2,N+1):
    fact[i]=fact[i-1]*i%mod
size=N+5
bit=[0]*size
def bit_add(i,delta):
    while i<size:
        bit[i]+=delta
        i+=i&-i
def bit_sum(i):
    s=0
    while i>0:
        s+=bit[i]
        i-=i&-i
    return s
for i in range(1,N+1):
    bit_add(i,1)
ans=1
for i,val in enumerate(perm):
    less=bit_sum(val-1)
    ans=(ans+less*fact[N-i-1])%mod
    bit_add(val,-1)
print(ans)
