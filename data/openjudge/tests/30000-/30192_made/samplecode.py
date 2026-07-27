# External reference: /practice/30192/statistics/
# Accepted submission: 52723659
# Source: http://cs101.openjudge.cn/practice/solution/52723659/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    W = int(input[ptr])
    ptr += 1
    n = int(input[ptr])
    ptr += 1
    t = []
    w = []
    for _ in range(n):
        ti = int(input[ptr])
        wi = int(input[ptr+1])
        t.append(ti)
        w.append(wi)
        ptr += 2
    
    size = 1 << n
    sumw = [0]*size
    maxt = [0]*size
    # 预处理所有子集的总重量、最大时间
    for s in range(size):
        sw = 0
        mt = 0
        for i in range(n):
            if s & (1 << i):
                sw += w[i]
                if t[i] > mt:
                    mt = t[i]
        sumw[s] = sw
        maxt[s] = mt
    
    INF = 10**18
    dp = [INF]*size
    dp[0] = 0
    
    for mask in range(size):
        if dp[mask] == INF:
            continue
        rem = ((1<<n)-1) ^ mask  # 剩余没过去的人
        # 枚举rem的所有非空子集sub
        sub = rem
        while sub:
            if sumw[sub] <= W:
                newmask = mask | sub
                if dp[newmask] > dp[mask] + maxt[sub]:
                    dp[newmask] = dp[mask] + maxt[sub]
            sub = (sub-1) & rem
    print(dp[(1<<n)-1])

if __name__ == "__main__":
    main()