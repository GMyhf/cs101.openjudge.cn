n, x = map(int,input().split())
a = list(map(int, input().split()))
dp = [set() for i in range(x + 1)]
queue = {0}
for coin in reversed(a):
    newqueue = set()
    for price in sorted(list(queue), reverse = True):
        newprice = price + coin
        if newprice > x: continue
        if newprice in queue: dp[newprice] &= dp[price] | {coin}
        else: dp[newprice] = dp[price] | {coin}
        newqueue.add(newprice)
    queue |= newqueue
    #print(*dp)
ans = sorted(list(dp[-1]))
print(len(ans))
print(*ans)