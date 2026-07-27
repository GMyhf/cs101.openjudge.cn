# External reference: statistics page /practice/20731/
# Accepted submission: 52201327
# Source: http://cs101.openjudge.cn/practice/solution/52201327/
# License: not declared on the submission page; no license is inferred.

m,n=map(int,input().split())
matrix=[]
for i in range(m):
    matrix.append(list(map(int,input().split())))
x,y=map(int,input().split())
x,y=x-1,y-1
if (x==0 and y==m-1) or (x!=0 and y!=m-1):
    ans=sum(matrix[0])+sum(matrix[m-1])
    for i in range(1,m-1):
        ans+=matrix[i][0]+matrix[i][n-1]
else:
    matrix[x],matrix[y]=matrix[y],matrix[x]
    ans=sum(matrix[0])+sum(matrix[m-1])
    for i in range(1,m-1):
        ans+=matrix[i][0]+matrix[i][n-1]
print(ans)