# External reference: statistics page /practice/01276/
# Accepted submission: 51703514
# Source: http://cs101.openjudge.cn/practice/solution/51703514/
# License: not declared on the submission page; no license is inferred.

import sys
def solve():
    data = sys.stdin.read().strip().split()
    idx = 0
    results = []
    while idx < len(data):
        cash = int(data[idx])
        idx += 1
        N = int(data[idx])
        idx += 1
        if N == 0:
            results.append("0")
            continue
        bills = []
        for _ in range(N):
            nk = int(data[idx])
            idx += 1
            Dk = int(data[idx])
            idx += 1
            bills.append((nk, Dk))
        items = []
        for nk, Dk in bills:
            k = 1
            while nk > 0:
                take = min(k, nk)
                items.append((take * Dk, take))
                nk -= take
                k <<= 1
        dp = [False] * (cash + 1)
        dp[0] = True
        for value, _ in items:
            for j in range(cash, value - 1, -1):
                if dp[j - value]:
                    dp[j] = True
        for j in range(cash, -1, -1):
            if dp[j]:
                results.append(str(j))
                break
    sys.stdout.write("\n".join(results))
if __name__ == "__main__":
    solve()
