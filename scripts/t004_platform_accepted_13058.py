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