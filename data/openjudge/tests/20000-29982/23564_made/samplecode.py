# External reference: http://cs101.openjudge.cn/practice/23564/statistics/
# Accepted submission: 52284871
# Source: http://cs101.openjudge.cn/practice/solution/52284871/
# License: not declared on the submission page; no license is inferred.

n=int(input())
def shulun(n):
    def pFactors(n):
        """Finds the prime factors of 'n'"""
        from math import sqrt
        pFact, limit, check, num = [], int(sqrt(n)) + 1, 2, n

        for check in range(2, limit):
            while num % check == 0:
                pFact.append(check)
                num /= check
        if num > 1:
            pFact.append(num)
        return pFact

    from collections import Counter
    p=Counter(pFactors(n))
    for key in p:
        if p[key]>=2:
            return 0
    x=len(p.keys())
    if x%2==0:
        return 1
    else:
        return -1
print(shulun(n))
