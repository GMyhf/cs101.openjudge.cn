# External reference: http://cs101.openjudge.cn/practice/01828/statistics/
# Accepted submission: 52005237
# Source: http://cs101.openjudge.cn/practice/solution/52005237/
# License: not declared on the submission page; no license is inferred.

while True:
    N = int(input())
    if N == 0:
        break
    monkeys = []
    for _ in range(N):
        x, y = map(int, input().split())
        monkeys.append((x, y))
    monkeys.sort(key = lambda p: (-p[0], -p[1]))
    cnt = 0
    max_y = float('-inf')
    for x, y in monkeys:
        if y > max_y:
            cnt += 1
            max_y = y
    print(cnt)
