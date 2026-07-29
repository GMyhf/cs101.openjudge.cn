# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1185: 炮兵阵地
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01185/
# License: not declared in source collection; no license is inferred.
import sys
N,M=map(int,input().split())
grid=[]
for _ in range(N):
    grid.append(list(input()))
# 状态a中的炮兵数
def num(a):
    return bin(a).count('1')
# 生成第i行所有合法的单行状态
def state(i):
    l=grid[i][:]
    x=0
    s=0
    while l:
        if l.pop()=='H':
            s+=2**x
        x+=1
    l1=[]
    for a in range(1<<M):
        if a&(a<<1) or a&(a>>1) or a&(a<<2) or a&(a>>2):
            continue
        if not a&s:
            l1.append(a)
    return l1
# N=1情形特判
if N==1:
    state0=state(0)
    print(max([num(a) for a in state0]))
    exit()
# 初始化
state2=state(0) # 上两行状态
state1=state(1) # 上一行状态
dp=[[0]*len(state2) for _ in range(len(state1))]
for i in range(len(state1)):
    for j in range(len(state2)):
        b=state1[i]
        c=state2[j]
        if not b&c:
            dp[i][j]=num(b)+num(c)
# dp的n方向维度是滚动的
for n in range(2,N):
    state0=state(n) # 当前行状态
    dp1=[[0]*len(state1) for _ in range(len(state0))]
    for i in range(len(state0)):
        a=state0[i]
        m=num(a)
        for j in range(len(state1)):
            b=state1[j]
            if a&b:
                continue
            for k in range(len(state2)):
                c=state2[k]
                if not a&c and not b&c:
                    dp1[i][j]=max(dp1[i][j],m+dp[j][k])
    dp=[row[:] for row in dp1]
    state2=state1[:]
    state1=state0[:]
print(max([max(row) for row in dp]))
