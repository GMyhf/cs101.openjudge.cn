# External reference: http://cs101.openjudge.cn/practice/01114/statistics/
# Accepted submission: 52288305
# Source: http://cs101.openjudge.cn/practice/solution/52288305/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。

from collections import defaultdict
def f(thing):
    multiply = 1
    i = 0
    while thing[i].isdigit():
        i += 1
    if i:
        multiply = int(thing[:i])
        thing = thing[i:]
    d = defaultdict(int)
    stack = []
    n = len(thing)
    idx = 0
    while idx < n:
        char = thing[idx]
        if char.isupper():
            if idx+1 < n and thing[idx+1].islower():
                stack.append(thing[idx:idx+2])
                idx += 2
                continue
            else:
                stack.append(char)
        elif char.isdigit():
            ori = idx
            while idx < n and thing[idx].isdigit():
                idx += 1
            num = int(thing[ori: idx])
            if stack and stack[-1] != ')':
                stack += [stack[-1]]*(num-1)
            else:
                stack.pop()
                temp = []
                while stack[-1] != '(':
                    temp.append(stack.pop())
                stack.pop()
                stack += temp*num
            continue
        else:
            # 修正：无倍数的括号组要就地消去这一对括号，否则外层倍数会误停在内层 '('
            if char == ')' and not (idx+1 < n and thing[idx+1].isdigit()):
                temp = []
                while stack[-1] != '(':
                    temp.append(stack.pop())
                stack.pop()
                stack += temp[::-1]
            else:
                stack.append(char)
        idx += 1
    for ele in stack:
        if ele not in '()':
            d[ele] += multiply
    return d
def fun(expr):
    d = defaultdict(int)
    l = expr.split('+')
    for x in l:
        dx = f(x)
        for k, v in dx.items():
            d[k] += v
    return d
materials = input()
d_m = fun(materials)
t = int(input())
for _ in range(t):
    produce = input()
    d_p = fun(produce)
    if d_m == d_p:
        print(f'{materials}=={produce}')
    else:
        print(f'{materials}!={produce}')
