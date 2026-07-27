# External reference: /practice/29946/statistics/
# Accepted submission: 52733385
# Source: http://cs101.openjudge.cn/practice/solution/52733385/
# License: not declared on the submission page; no license is inferred.

s = input().strip()
k = int(input())

stack = []
for c in s:
    # 还能删，且栈顶比当前大，就删栈顶
    while k > 0 and stack and stack[-1] > c:
        stack.pop()
        k -= 1
    stack.append(c)

# 如果还剩删除次数，从末尾删
if k > 0:
    stack = stack[:-k]

# 去掉前导零
res = ''.join(stack).lstrip('0')

# 全零情况输出 0
print(res if res else '0')