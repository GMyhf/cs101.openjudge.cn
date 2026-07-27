# External reference: statistics page /practice/28336/
# Accepted submission: 52734521
# Source: http://cs101.openjudge.cn/practice/solution/52734521/
# License: not declared on the submission page; no license is inferred.

s = input().strip()
stack = []

for c in s:
    # 如果栈不为空，且栈顶和当前字符相同，就消除（弹出栈顶）
    if stack and stack[-1] == c:
        stack.pop()
    else:
        stack.append(c)

# 拼接结果
res = ''.join(stack)
print(res if res else 'Empty')