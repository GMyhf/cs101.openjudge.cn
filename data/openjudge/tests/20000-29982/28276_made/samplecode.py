# External reference: http://cs101.openjudge.cn/practice/28276/statistics/
# Accepted submission: 52720719
# Source: http://cs101.openjudge.cn/practice/solution/52720719/
# License: not declared on the submission page; no license is inferred.

import sys
sys.setrecursionlimit(10**6)
def data():
    for line in sys.stdin.buffer:
        for token in line.split():
            yield token
class UnionFind:
    def __init__(self,n):
        self.parent=list(range(n))
        self.rank=[0]*n
    def find(self,x):
        if self.parent[x]!=x:
            self.parent[x]=self.find(self.parent[x])
        return self.parent[x]
    def union(self,x,y):
        rx,ry=self.find(x),self.find(y)
        if rx!=ry:
            if self.rank[rx]>self.rank[ry]:
                self.parent[ry]=rx
            elif self.rank[rx]<self.rank[ry]:
                self.parent[rx]=ry
            else:
                self.parent[ry]=rx
                self.rank[rx]+=1
def main():
    uf=UnionFind(26)
    it=data()
    n=int(next(it))
    wait=[]
    for _ in range(n):
        inp=next(it).decode()
        x=ord(inp[0])-97
        y=ord(inp[-1])-97
        if inp[1]=='=':
            uf.union(x,y)
        else:
            wait.append((x,y))
    for x,y in wait:
        if uf.find(x)==uf.find(y):
            return False
    return True
print(main())
