# External reference: cs101.openjudge.cn practice/04120 statistics, Accepted solution 52470090.
# Source: http://cs101.openjudge.cn/practice/solution/52470090/
# License: no explicit license stated on the submission page; retained as an external platform reference.

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
