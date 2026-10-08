# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原 samplecode（来源 /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md）是 O(N·轮数) 的分组贪心，
# 在 N=1e5 的满规模数据上超时；数据审计时换成与之等价的 O(N log N) 写法（与 producecase.py 的 REFERENCE_SOURCE 相同，
# 已与旧版、O(N^2) 暴力及 BFS 穷举在小/中规模数据上逐组对拍一致）。
# 拓扑序视角：i<j 且 |h_i-h_j|>D 时 i 必须在 j 前；每次取入度为 0 的最小身高（同值取靠左者）。
# 入度按身高排名放进带懒标记的线段树：删掉 v 后，所有身高在 [v-D, v+D] 之外的未处理者入度减 1。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
from bisect import bisect_left, bisect_right
def main():
    data=sys.stdin.buffer.read().split(); n=int(data[0]); D=int(data[1]); h=list(map(int,data[2:2+n]))
    order=sorted(range(n),key=lambda i:(h[i],i)); rank=[0]*n
    for r,i in enumerate(order): rank[i]=r
    vals=[h[i] for i in order]
    # 初始入度：i<j 且 |h_i-h_j|>D 的个数（BIT 按值排名计数）
    bit=[0]*(n+1); indeg=[0]*n
    def add(p):
        p+=1
        while p<=n: bit[p]+=1; p+=p&-p
    def pre(p):  # count ranks < p
        s=0
        while p>0: s+=bit[p]; p-=p&-p
        return s
    for j in range(n):
        lo=bisect_left(vals,h[j]-D); hi=bisect_right(vals,h[j]+D)
        indeg[rank[j]]=pre(lo)+(j-pre(hi))
        add(rank[j])
    size=1
    while size<n: size*=2
    INF=float('inf')
    mn=[INF]*(2*size); lz=[0]*(2*size)
    for r in range(n): mn[size+r]=indeg[r]
    for x in range(size-1,0,-1): mn[x]=min(mn[2*x],mn[2*x+1])
    def upd(l,r,v,x=1,a=0,b=None):
        if b is None: b=size
        if r<=a or b<=l: return
        if l<=a and b<=r: mn[x]+=v; lz[x]+=v; return
        m=(a+b)//2; upd(l,r,v,2*x,a,m); upd(l,r,v,2*x+1,m,b); mn[x]=min(mn[2*x],mn[2*x+1])+lz[x]
    out=[]
    for _ in range(n):
        # 找最左（值最小、同值下标最小）入度为 0 的叶子
        x=1; acc=0
        assert mn[1]==0
        while x<size:
            acc+=lz[x]
            x=2*x if mn[2*x]+acc==0 else 2*x+1
        r=x-size; out.append(vals[r])
        # 删除：设为 INF
        y=x; mn[y]=INF
        y//=2
        while y: mn[y]=min(mn[2*y],mn[2*y+1])+lz[y]; y//=2
        v=vals[r]
        lo=bisect_left(vals,v-D); hi=bisect_right(vals,v+D)
        if lo>0: upd(0,lo,-1)
        if hi<n: upd(hi,n,-1)
    sys.stdout.write('\n'.join(map(str,out))+'\n')
main()
