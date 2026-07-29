# External reference: http://cs101.openjudge.cn/practice/02000/statistics/
# Accepted submission: 52824529
# Source: http://cs101.openjudge.cn/practice/solution/52824529/
# License: not declared on the submission page; no license is inferred.

def main(N):
    daygroups = [i for i in range(1,5000)]

    total_days = 0
    coins = 0

    for day in daygroups:
        for i in range(day):
            total_days += 1
            coins += day
            # print(total_days, coins)
            if total_days == N:
                break
        if total_days == N:
            break

    return total_days, coins

while True:
    N = int(input())
    if N == 0: break
    print(*main(N))
