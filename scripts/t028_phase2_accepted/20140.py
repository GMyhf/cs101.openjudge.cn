# External reference: http://cs101.openjudge.cn/practice/20140/statistics/
# Accepted submission: 52716352
# Source: http://cs101.openjudge.cn/practice/solution/52716352/
# License: not declared on the submission page; no license is inferred.

def translate(string:list):
    num=""
    for i in range(len(string)):
        if string[i].isdigit():
            num+=string[i]
        else:
            string=string[i:]
            break
    return int(num)*string

secret=list(input())
stack=[]
for char in secret:
    if char!="]":
        stack.append(char)
    else:
        merging=[]
        while stack:
            last=stack.pop()
            if last=="[":
                break
            merging.append(last)
        merging.reverse()
        stack.extend(translate(merging))
print("".join(stack))
