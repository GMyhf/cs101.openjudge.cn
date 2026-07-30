# External reference: http://cs101.openjudge.cn/practice/18107/statistics/
# Accepted submission: 51275473
# Source: http://cs101.openjudge.cn/practice/solution/51275473/
# License: not declared on the submission page; no license is inferred.

def generate_primes(limit):
    prime = [True]*(limit+1)
    p = 2
    while p*p <= limit:
        if prime[p]:
            for i in range(p*2, limit+1, p):
                prime[i] = False
        p += 1
    return [p for p in range(2, limit+1) if prime[p]]
T = int(input())
for _ in range(T):
    m, n = map(int, input().split())
    p1 = generate_primes(m-1)
    p2 = generate_primes(n)
    res = p2[len(p1):]
    if res:
        print(*res)
    else:
        print(-1)
