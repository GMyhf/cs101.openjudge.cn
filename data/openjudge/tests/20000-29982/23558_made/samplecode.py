# External reference: http://cs101.openjudge.cn/practice/23558/statistics/
# Accepted submission: 51988550
# Source: http://cs101.openjudge.cn/practice/solution/51988550/
# License: not declared on the submission page; no license is inferred.

lis = list(map(int,input().split()))
n,k,l = lis[0],lis[1],lis[2]
dic = {}
for _ in range(k):
    A = list(map(int,input().split()))
    if A[0] not in dic:
        dic[A[0]] = []
    dic[A[0]].append(A[1])
    if A[1] not in dic:
        dic[A[1]] = []
    dic[A[1]].append(A[0])
for x in dic:
    dic[x].sort() #从小到大排序

start = int(input()) #起点
if start not in dic:
    dic[start] = []
def dfs(start,visited=set(),li=[],depth=0):
    if depth <=l:
        if start not in visited:
            visited.add(start)
            li.append(start)
            for p in dic[start]:
                dfs(p,visited,li,depth+1)
    return li
A = dfs(start,set(),[],0)
s = ""
for x in A:
    s += str(x)+" "
print(s[:-1])
