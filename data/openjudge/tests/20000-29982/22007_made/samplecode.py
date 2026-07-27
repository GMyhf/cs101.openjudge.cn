# External reference: statistics page /practice/22007/
# Accepted submission: 52245294
# Source: http://cs101.openjudge.cn/practice/solution/52245294/
# License: not declared on the submission page; no license is inferred.

# External reference: statistics page /practice/22007/
# Accepted submission: 52245294
# Source: http://cs101.openjudge.cn/practice/solution/52245294/
# License: not declared on the submission page; no license is inferred.

n=int(input())
board=[[0]*n for i in range(n)]
def issafe(lines,x,y):
    for i in range(len(lines)):
        if i-lines[i]==x-y or i+lines[i]==x+y:
            return False
    return True

ans=[]
def dfs(lines,count):
    if count==n:
        ans.append(lines[:])
        return
    if len(lines)>n:
        return
    for j in range(n):
        if j not in lines and issafe(lines,len(lines),j):
            lines.append(j)
            dfs(lines,count+1)
            lines.pop()

dfs([],0)
ans.sort()
if not ans:
    print('NO ANSWER')
else:
    for lines in ans:
        print(*lines)