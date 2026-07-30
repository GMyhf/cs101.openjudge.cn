# External reference: http://cs101.openjudge.cn/practice/28190/statistics/
# Accepted submission: 52726662
# Source: http://cs101.openjudge.cn/practice/solution/52726662/
# License: not declared on the submission page; no license is inferred.

n = int(input())
arr = [int(input()) for _ in range(n)]
ans = -1
# 预处理maxs和mins
maxs = [n]*n
stack = []
for i in range(n-1,-1,-1):
    while stack and arr[stack[-1]] <= arr[i]:
        stack.pop()
    maxs[i] = stack[-1] if stack else n
    stack.append(i)
mins = [n]*n
stack = []
for i in range(n-1,-1,-1):
    while stack and arr[stack[-1]] > arr[i]:
        stack.pop()
    mins[i] = stack[-1] if stack else n
    stack.append(i)
right = 0
for i in range(n):
    lmt = mins[i]# 右端点受到左端点最小值条件限制
    if right < i:#右端点必须在左端点右侧
        right = i
    while right < lmt:
        nxt = maxs[right]#扩展右端点
        if nxt < lmt:
            right = nxt
        else:
            break
    ans = max(ans,right-i+1)
print(ans)
