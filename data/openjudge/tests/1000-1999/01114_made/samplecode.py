# External reference: http://cs101.openjudge.cn/practice/01114/statistics/
# Accepted submission: 52288305
# Source: http://cs101.openjudge.cn/practice/solution/52288305/
# License: not declared on the submission page; no license is inferred.

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
