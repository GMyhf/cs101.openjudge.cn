# Self-written reference: minimum s-t cut on the grid wall graph
# Oracle: independent exhaustive cut enumeration for generated small grids

import sys,itertools
def solve():
    a=list(map(int,sys.stdin.read().split())); p=0; n,m=a[p],a[p+1]; p+=2
    g=[a[p+i*m:p+(i+1)*m] for i in range(n)]; p+=n*m
    v=[a[p+i*(m+1):p+(i+1)*(m+1)] for i in range(n)]; p+=n*(m+1)
    h=[a[p+i*m:p+(i+1)*m] for i in range(n+1)]
    k=n*m; need={i*m+j for i in range(n) for j in range(m) if g[i][j]}; ans=10**30
    for mask in range(1<<k):
        if any(not(mask>>u&1) for u in need): continue
        seen={next(iter(need))}; q=list(seen)
        for u in q:
            i,j=divmod(u,m)
            for z in (u-1 if j else -1, u+1 if j+1<m else -1,
                      u-m if i else -1, u+m if i+1<n else -1):
                if z >= 0 and mask>>z&1 and z not in seen:
                    seen.add(z); q.append(z)
        if len(seen) != bin(mask).count('1'): continue
        cost=0
        for i in range(n):
            for j in range(m):
                u=i*m+j
                if j==0 and mask>>u&1: cost+=v[i][0]
                if j==m-1 and mask>>u&1: cost+=v[i][m]
                if i==0 and mask>>u&1: cost+=h[0][j]
                if i==n-1 and mask>>u&1: cost+=h[n][j]
                if j+1<m and ((mask>>u&1)!=(mask>>(u+1)&1)): cost+=v[i][j+1]
                if i+1<n and ((mask>>u&1)!=(mask>>(u+m)&1)): cost+=h[i+1][j]
        ans=min(ans,cost)
    print(ans)
if __name__=='__main__': solve()
