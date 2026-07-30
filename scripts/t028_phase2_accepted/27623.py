# External reference: http://cs101.openjudge.cn/practice/27623/statistics/
# Accepted submission: 52408063
# Source: http://cs101.openjudge.cn/practice/solution/52408063/
# License: not declared on the submission page; no license is inferred.

#状态x,y，先手是否必胜？
def dfs(x,y):
    if x==y:
        return True
    elif x>=2*y:
        return True
    else:
        return (not dfs(y,x-y))

while True:
    a,b=[int(i) for i in input().split()]
    if a==0 and b==0:
        break
    if a<b:
        a,b=b,a
    if dfs(a,b):
        print("win")
    else:
        print("lose")
