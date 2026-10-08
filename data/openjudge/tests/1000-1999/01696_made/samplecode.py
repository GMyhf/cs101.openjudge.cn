# External reference: http://cs101.openjudge.cn/practice/01696/statistics/
# Accepted submission: 43692664
# Source: http://cs101.openjudge.cn/practice/solution/43692664/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原代码用浮点 acos 排转角：共线时余弦略大于 1 会抛 math domain error，且共线时不按距离决胜。
# 改为精确整数叉积：每步挑「其余点都在它左侧」的那个点，共线时先走近的。

for _ in range(int(input())):
    try:
        n=int(input())
    except:
        n=int(input())
    l=[tuple(map(int,input().split())) for i in range(n)]
    cur=min(l,key=lambda p:p[2])
    ans=[n,cur[0]]
    l.remove(cur)
    while l:
        best=l[0]
        for q in l[1:]:
            ax,ay=best[1]-cur[1],best[2]-cur[2]
            bx,by=q[1]-cur[1],q[2]-cur[2]
            cr=ax*by-ay*bx
            if cr<0 or (cr==0 and bx*bx+by*by<ax*ax+ay*ay):
                best=q
        ans.append(best[0])
        l.remove(best)
        cur=best
    print(*ans)
