# External reference: http://cs101.openjudge.cn/practice/03177/statistics/
# Accepted submission: 50653216
# Source: http://cs101.openjudge.cn/practice/solution/50653216/
# License: not declared on the submission page; no license is inferred.

def primes(limit):
    l = [False]*2 + [True]*(limit-1)
    for p in range(2, int(limit**0.5)+1):
        if l[p]:
            for i in range(p*2, limit+1, p):
                l[i] = False
    return [1 if x else 0 for x in l]
X, Y = map(int, input().split())
L = primes(max(X, Y))
print(max(sum(L[X:]), sum(L[Y:])))
