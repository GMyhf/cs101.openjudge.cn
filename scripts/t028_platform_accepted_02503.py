# External reference: http://cs101.openjudge.cn/practice/02503/statistics/
# Accepted submission: 51766135
# Source: http://cs101.openjudge.cn/practice/solution/51766135/
# License: not declared on the submission page; no license is inferred.

d = {}
while True:
    inp = input().split()
    if not inp:
        break
    d[inp[1]] = inp[0]
while True:
    try:
        inp = input()
        if inp not in d:
            print('eh')
        else:
            print(d[inp])
    except EOFError:
        break
