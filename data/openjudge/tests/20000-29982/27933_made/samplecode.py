# External reference: statistics page /practice/27933/
# Accepted submission: 52735532
# Source: http://cs101.openjudge.cn/practice/solution/52735532/
# License: not declared on the submission page; no license is inferred.

n = int(input())
stack = []
res = 0
target = 1

for _ in range(2 * n):
    parts = input().split()
    if parts[0] == 'add':
        x = int(parts[1])
        stack.append(x)
    else:
        if stack:
            # 栈顶正好是要弹出的数字 → 正常弹出
            if stack[-1] == target:
                stack.pop()
            else:
                # 必须重排一次
                res += 1
                stack = []  # 重排后栈内元素有序，直接清空
        target += 1

print(res)