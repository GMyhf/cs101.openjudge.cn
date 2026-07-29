# External reference: http://cs101.openjudge.cn/practice/02915/statistics/
# Accepted submission: 52675051
# Source: http://cs101.openjudge.cn/practice/solution/52675051/
# License: not declared on the submission page; no license is inferred.

while True:
    try:
        n = int(input())
    except Exception:
        break
    strings = []
    for _ in range(n):
        s = input()
        if s == 'stop':
            break
        strings.append(s)
    strings.sort(key = lambda x: len(x))
    for s in strings:
        print(s)
