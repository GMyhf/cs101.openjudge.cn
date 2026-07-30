# External reference: http://cs101.openjudge.cn/practice/29952/statistics/
# Accepted submission: 52722952
# Source: http://cs101.openjudge.cn/practice/solution/52722952/
# License: not declared on the submission page; no license is inferred.

data = input()

stack = []
ans = 0
tot = 0

for s in data:
    if s == ')':
        a = 0
        while stack and stack[-1] !='(' and stack[-1] != ')':
            b = stack.pop()
            a += b
        if not stack:
            stack.append(a)
            stack.append(s)
            tot = max(tot, a)


        elif stack[-1] == ')':
            stack.append(a)
            stack.append(s)
            tot = max(tot, a)


        else:
            stack.pop()
            a += 2
            while stack and stack[-1] !='(' and stack[-1] != ')':
                c = stack.pop()
                a += c

            stack.append(a)
            tot = max(tot, a)

    if s == '(':
        stack.append(s)

print(tot)
