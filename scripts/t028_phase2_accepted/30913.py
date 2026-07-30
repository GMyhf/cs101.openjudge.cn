# External reference: http://cs101.openjudge.cn/practice/30913/statistics/
# Accepted submission: 52838694
# Source: http://cs101.openjudge.cn/practice/solution/52838694/
# License: not declared on the submission page; no license is inferred.

import math
def weigh(weu):
    t=(math.isqrt(8*weu+1)-1)//2
    while (t + 1) * t // 2 < weu:
        t += 1
    wt=t*weu-(t-1)*t*(t+1)//6
    return wt
n,m=map(int,input().split())
g=[[]for _ in range(n)]
for _ in range(m):
    u,v,w=map(int,input().split())
    g[u-1].append((v-1,w))
s=int(input())-1

import sys
sys.setrecursionlimit(10**6)

def tar(n,g):
    index=0
    idx=[-1]*n
    low=[0]*n
    on_stack=[False]*n
    stack=[]
    comp=[-1]*n
    scc_cnt=0

    def dfs(v):
        nonlocal index,scc_cnt
        idx[v]=low[v]=index
        index+=1
        stack.append(v)
        on_stack[v]=True

        for to,_ in g[v]:
            if idx[to]==-1:
                dfs(to)
                low[v]=min(low[to],low[v])
            elif on_stack[to]:
                low[v]=min(low[v],idx[to])
        if low[v]==idx[v]:
            while True:
                w=stack.pop()
                on_stack[w]=False
                comp[w]=scc_cnt
                if w==v:
                    break
            scc_cnt += 1
    for v in range(n):
        if idx[v]==-1:
            dfs(v)
    return  comp ,scc_cnt

comp,scc_cnt=tar(n,g)

dag_g=[dict() for _ in range(scc_cnt)]
scc_wei=[0]*scc_cnt
for u in range(n):
    u_scc= comp[u]
    # scc_wei[u_scc]+=weigh(u)
    for v,w in g[u]:
        v_scc= comp[v]
        if u_scc==v_scc:
            scc_wei[u_scc]+=weigh(w)
        else:
            if v_scc not in dag_g[u_scc] or dag_g[u_scc][v_scc]<w:
                dag_g[u_scc][v_scc]=w
dag_list = [[] for _ in range(scc_cnt)]
for u in range(scc_cnt):
    for v, w in dag_g[u].items():
        dag_list[u].append((v, w))


dp=[0]*scc_cnt
for u in range(scc_cnt):
    best=0
    for v,w in dag_list[u]:
        if w+dp[v]>best:
            best=w+dp[v]
    dp[u]=scc_wei[u]+best


stat=comp[s]
print(dp[stat])
