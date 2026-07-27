# External reference: statistics page /practice/20974/
# Accepted submission: 52686810
# Source: http://cs101.openjudge.cn/practice/solution/52686810/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/20974/
# Accepted submission: 52686810
# Source: http://cs101.openjudge.cn/practice/solution/52686810/
# License: not declared on the submission page; no license is inferred.

m, s, c = map(int, input().split())
cows = [int(input()) for _ in range(c)]
if c == 0:
    print(0)
else:
    cows.sort()
    if m >= c:
        print(c)
    else:
        total = cows[-1] - cows[0] + 1
        gaps = [cows[i] - cows[i-1] - 1 for i in range(1, c)]
        gaps.sort(reverse=True)
        total -= sum(gaps[:m-1])
        print(total)