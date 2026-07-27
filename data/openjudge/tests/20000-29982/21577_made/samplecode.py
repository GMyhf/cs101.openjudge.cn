# External reference: statistics page /practice/21577/
# Accepted submission: 52726677
# Source: http://cs101.openjudge.cn/practice/solution/52726677/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/21577/
# Accepted submission: 52726677
# Source: http://cs101.openjudge.cn/practice/solution/52726677/
# License: not declared on the submission page; no license is inferred.


def max_area(line,c):
    stack=[-1]
    m=-114514
    line.append(0)
    for i in range(c+1):
        while stack[-1]!=-1 and line[i]<line[stack[-1]]:
            idx=stack.pop()
            now_area=line[idx]*(i-stack[-1]-1)
            if now_area>m:
                m=now_area
        stack.append(i)
    return m

ans=float("-inf")
r,c=map(int,input().split())
trees=[]
for i in range(r):
    trees.append(list(map(int,input().split())))
matrix=[[0 for _ in range(c)] for _ in range(r)]
for i in range(c):
    if trees[0][i]==0:
        matrix[0][i]=1
for i in range(c):
    for j in range(1,r):
        if trees[j][i]==0:
            matrix[j][i]=matrix[j-1][i]+1
        else:
            matrix[j][i]=0
for line in matrix:
    ans=max(ans,max_area(line,c))
print(ans)
