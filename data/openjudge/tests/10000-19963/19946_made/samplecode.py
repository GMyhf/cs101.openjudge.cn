# External reference: statistics page /practice/19946/
# Accepted submission: 51285749
# Source: http://cs101.openjudge.cn/practice/solution/51285749/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/19946 statistics, Accepted solution 51285749.
# Source: http://cs101.openjudge.cn/practice/solution/51285749/
# Statistics: http://cs101.openjudge.cn/practice/19946/statistics/
# License: not declared on submission page; no license inferred
m, n = map(int, input().split())
workers = [int(x) for x in input().split()]
hamburgers = [int(x) for x in input().split()]
workers.sort()
hamburgers.sort()
i, j, res = 0, 0, 0
while i < m and j < n:
    if workers[i] >= hamburgers[j]:
        res += 1
        i += 1
        j += 1
    else:
        i += 1
print(res)
