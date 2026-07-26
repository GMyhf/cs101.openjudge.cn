# External reference: statistics page /practice/13058/
# Accepted submission: 51209375
# Source: http://cs101.openjudge.cn/practice/solution/51209375/
# License: not declared on the submission page; no license is inferred.

N = int(input())
heights = []
for _ in range(N):
    heights.append(int(input()))
stack = []
ans = 0
for i in range(N):
    h = heights[i]
    while stack and stack[-1][0] <= h:
        stack.pop()
    ans += len(stack)
    stack.append((h, i))
print(ans)