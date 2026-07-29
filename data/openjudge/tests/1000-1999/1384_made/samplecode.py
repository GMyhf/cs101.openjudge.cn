# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1384: Piggy-Bank
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/01384/
# License: not declared in source collection; no license is inferred.
INF = float("inf")
TC = int(input())
for _ in range(TC):
    E, F = map(int, input().split())
    N = int(input())
    coins = []
    for _ in range(N):
        p, w = map(int, input().split())
        coins.append((p, w))

    amount = F - E
    dp = [0] + [INF]*amount

    for i in range(N):
        p, w = coins[i]
        for j in range(w, amount+1):
            if dp[j-w] != INF:
                dp[j] = min(dp[j], dp[j-w] + p)

    #print(dp)
    if dp[-1] != INF:
        print(f"The minimum amount of money in the piggy-bank is {dp[-1]}.")
    else:
        print(f"This is impossible.")
