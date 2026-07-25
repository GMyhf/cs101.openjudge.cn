# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
N,K=map(int,input().split())
def num(a):
	# 状态a中的国王数
    return bin(a).count('1')
# 存储所有单行合法的状态
state=[]
for a in range(1<<N):
    if a&(a<<1):
        continue
    k=num(a)
    if k>K:
        continue
    state.append(a)
M=len(state)
# 存储相邻两行合法的状态
conflict=[[False]*M for _ in range(M)]
for i in range(M):
    for j in range(M):
        a=state[i]
        b=state[j]
        if a&b==0 and a&(b<<1)==0 and a&(b>>1)==0:
            conflict[i][j]=True
dp=[[0]*M for _ in range(K+1)]
for i in range(M):
    a=state[i]
    dp[num(a)][i]=1
for _ in range(N-1):
    dp1=[[0]*M for _ in range(K+1)]
    for i in range(M):
        a=state[i]
        k=num(a)
        for m in range(K+1-k):
            for j in range(M):
                if conflict[i][j]:
                    dp1[k+m][i]+=dp[m][j]
    dp=dp1
print(sum(dp[-1]))
