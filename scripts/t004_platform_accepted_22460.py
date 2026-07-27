# External reference: statistics page /practice/22460/
# Accepted submission: 45199466
# Source: http://cs101.openjudge.cn/practice/solution/45199466/
# License: not declared on the submission page; no license is inferred.

def valid(n,ls):
    stack = []
    for cha in ls:
        if cha == '#' :
            if not stack:
                return False
            stack[-1] -= 1
        else:
            if not stack and cha != ls[0]:
                return False
            if stack:
                stack[-1] -= 1
            stack.append(2)
        
        while stack and stack[-1] == 0:
            stack.pop()
    
    return not stack

while True:
    n = int(input())
    if n == 0:
        break
    ls = input().split()
    
    print('T' if valid(n,ls) else 'F')