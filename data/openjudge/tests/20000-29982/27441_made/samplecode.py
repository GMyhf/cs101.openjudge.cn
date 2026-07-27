# External reference: statistics page /practice/27441/
# Accepted submission: 52735735
# Source: http://cs101.openjudge.cn/practice/solution/52735735/
# License: not declared on the submission page; no license is inferred.

def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    N = int(input[ptr])
    M = int(input[ptr+1])
    ptr +=2
    p = list(map(int,input[ptr:ptr+M]))
    ptr += M
    num = list(map(int,input[ptr:ptr+M]))

    INF = 10**18
    dp = [INF]*(N+1)
    dp[0] = 0

    for i in range(M):
        pi = p[i]
        ci = num[i]
        # 二进制优化多重背包
        k = 1
        rest = ci
        while rest>0:
            take = min(k, rest)
            cost = take*pi
            cnt = take
            # 倒序
            for v in range(N, cost-1, -1):
                if dp[v-cost] + cnt < dp[v]:
                    dp[v] = dp[v-cost]+cnt
            rest -= take
            k *=2
    if dp[N]==INF:
        print("Fail")
    else:
        print(dp[N])

if __name__=="__main__":
    main()