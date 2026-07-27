# External reference: /practice/29677/statistics/
# Accepted submission: 52733700
# Source: http://cs101.openjudge.cn/practice/solution/52733700/
# License: not declared on the submission page; no license is inferred.

import sys
input = sys.stdin.read
sys.setrecursionlimit(1 << 25)

class DSU:
    def __init__(self, n):
        self.fa = list(range(n+1))
    def find(self, x):
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]
    def union(self, x, y):
        fx = self.find(x)
        fy = self.find(y)
        if fx != fy:
            self.fa[fy] = fx

def main():
    data = list(map(int, input().split()))
    ptr = 0
    T = data[ptr]
    ptr +=1
    for _ in range(T):
        N = data[ptr]
        ptr +=1
        t = data[ptr:ptr+N]
        ptr +=N
        d = data[ptr:ptr+N]
        ptr +=N
        dsu = DSU(N)
        for i in range(1,N+1):
            di = d[i-1]
            p1 = i + di
            if 1<=p1<=N:
                dsu.union(i,p1)
            p2 = i - di
            if 1<=p2<=N:
                dsu.union(i,p2)
        ok = True
        for idx in range(N):
            pos = idx+1
            tar = t[idx]
            if dsu.find(pos) != dsu.find(tar):
                ok = False
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    main()