# External reference: http://cs101.openjudge.cn/practice/18159/statistics/
# Accepted submission: 51809745
# Source: http://cs101.openjudge.cn/practice/solution/51809745/
# License: not declared on the submission page; no license is inferred.

T=int(input())
nums=[]
ans=[[] for _ in range(T)]
for i in range(T):
    nums.append((int(input()),i))
nums.sort(key=lambda x:x[0])
def euler_sieve(n):
    is_prime=[True]*(n+1)
    is_prime[0]=is_prime[1]=False
    primes=[]
    for i in range(2,n+1):
        if is_prime[i]:
            primes.append(i)
        for p in primes:
            if i*p>n:
                break
            is_prime[i*p]=False
            if i%p==0:
                break
    return primes
p=euler_sieve(nums[-1][0])
loc=0
re=[]
for num,idx in nums:
    while loc<len(p) and p[loc]<num:
        if str(p[loc])[-1]=='1':
            re.append(p[loc])
        loc+=1
    ans[idx]=re[:]
for i,l in enumerate(ans):
    print(f'Case{i+1}:')
    if l:
        print(*l)
    else:
        print('NULL')
