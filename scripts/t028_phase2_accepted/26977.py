# External reference: http://cs101.openjudge.cn/practice/26977/statistics/
# Accepted submission: 52739982
# Source: http://cs101.openjudge.cn/practice/solution/52739982/
# License: not declared on the submission page; no license is inferred.

n=int(input())
line=list(map(int,input().split()))
stack=[]
rain=0
for i in range(n):
    #维护一个递减栈
    h=line[i]
    while stack and line[stack[-1]]<h:
        l=stack.pop()
        if stack:
            j=stack[-1]
            rain+=(min(line[j],h)-line[l])*(i-stack[-1]-1)
    stack.append(i)
print(rain)
