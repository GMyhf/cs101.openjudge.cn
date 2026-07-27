# External reference: statistics page /practice/28200/
# Accepted submission: 52734593
# Source: http://cs101.openjudge.cn/practice/solution/52734593/
# License: not declared on the submission page; no license is inferred.

import sys

input = sys.stdin.read
data = input().split()

N = int(data[0])
D = int(data[1])
MOD = 998244353

if D == 0:
    print(0)
    sys.exit(0)

# Precompute powers of 2
MAXN = max(N, D) + 5
pw = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    pw[i] = (pw[i-1] * 2) % MOD

# ans[i+1] = sum for left path length 0 to i
ans = [0] * (D + 2)
for i in range(D + 1):
    j = D - i
    l = pw[max(0, i - 1)]
    r = pw[max(0, j - 1)]
    ans[i + 1] = (ans[i] + 2 * l * r % MOD) % MOD

res = 0
for dep in range(1, N + 1):  # depth from 1 to N (root depth 0, but we skip root? wait)
    # In code: for(int i=1;i<=n;i++)  i is depth?
    l = max(0, dep + D - N)
    r = min(D, N - dep)
    if l > r:
        continue
    # res = number for one node at this depth
    temp = (ans[min(D, N - dep) + 1] - ans[max(0, dep + D - N)] + MOD) % MOD
    # multiply by number of nodes at this depth: 2^{dep-1}
    res = (res + pw[dep - 1] * temp % MOD) % MOD

print(res)