# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
MOD = 10**9 + 7

import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it)); L = int(next(it)); M_val = int(next(it))
    start = [int(next(it)) for _ in range(N)]
    mid = [int(next(it)) for _ in range(N)]
    end = [int(next(it)) for _ in range(N)]
    
    M = M_val
    
    # Precompute start_mod
    start_mod = [0] * M
    for x in start:
        start_mod[x % M] += 1
    
    # Precompute mid_mod
    mid_mod = [0] * M
    for x in mid:
        mid_mod[x % M] += 1
    
    # Precompute last_cost = mid + end
    last_mod = [0] * M
    for i in range(N):
        cost = (mid[i] + end[i]) % M
        last_mod[cost] += 1

    # Convolution function
    def convolve(a, b):
        res = [0] * M
        for i in range(M):
            if a[i]:
                ai = a[i]
                for j in range(M):
                    if b[j]:
                        res[(i + j) % M] = (res[(i + j) % M] + ai * b[j]) % MOD
        return res

    # Identity kernel
    identity = [0] * M
    identity[0] = 1

    if L == 2:
        cur = start_mod[:]
    else:
        # Compute mid_mod^(L-2) under convolution
        def power_conv(base, exp):
            result = identity[:]
            base = base[:]
            while exp:
                if exp & 1:
                    result = convolve(result, base)
                base = convolve(base, base)
                exp //= 2
            return result
        
        mid_power = power_conv(mid_mod, L - 2)
        cur = convolve(start_mod, mid_power)
    
    # Now combine with last_mod
    ans = 0
    for r in range(M):
        needed = (M - r) % M
        ans = (ans + cur[r] * last_mod[needed]) % MOD
    
    print(ans)

if __name__ == '__main__':
    main()
