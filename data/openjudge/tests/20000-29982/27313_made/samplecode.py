# External reference: statistics page /practice/27313/
# Accepted submission: 52520937
# Source: http://cs101.openjudge.cn/practice/solution/52520937/
# License: not declared on the submission page; no license is inferred.

MOD = 10**9 + 7
max_n = 50

# 预处理阶乘和逆阶乘
fact = [1] * (max_n + 1)
for i in range(1, max_n + 1):
    fact[i] = fact[i-1] * i % MOD

inv_fact = [1] * (max_n + 1)
inv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)
for i in range(max_n - 1, -1, -1):
    inv_fact[i] = inv_fact[i+1] * (i+1) % MOD

def compute_f(sub_s):
    """计算满足符号序列sub_s的排列数"""
    m = len(sub_s)
    if m == 0:
        return 1  # 空序列对应1个元素，只有1种排列

    # dp[i][j]：长度为i的排列，满足前i-1个符号，以第j小元素结尾的数量（1-based）
    dp = [[0] * (m + 2) for _ in range(m + 2)]
    dp[1][1] = 1

    for i in range(2, m + 2):
        # 计算前缀和优化求和
        prefix = [0] * i
        for k in range(1, i):
            prefix[k] = (prefix[k-1] + dp[i-1][k]) % MOD

        sym = sub_s[i-2]
        for j in range(1, i + 1):
            if sym == '<':
                # 前一个元素小于当前元素，求和1..j-1
                dp[i][j] = prefix[j-1] if j-1 >= 1 else 0
            else:  # '>'
                # 前一个元素大于当前元素，求和j..i-1
                dp[i][j] = (prefix[i-1] - prefix[j-1]) % MOD

    # 总和即为该符号序列的排列数
    res = 0
    for j in range(1, m + 2):
        res = (res + dp[m+1][j]) % MOD
    return res

def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    n = int(input[ptr])
    ptr +=1
    p = list(map(int, input[ptr:ptr+n]))
    ptr +=n

    # 计算逆置换pos：pos[x]是元素x在p中的位置
    pos = [0] * n
    for i in range(n):
        pos[p[i]] = i

    # 检查每个边界是否恰好有一个元素向右穿过
    valid = True
    for i in range(n-1):
        cnt = 0
        for x in range(n):
            if x <= i < pos[x]:
                cnt +=1
        if cnt != 1:
            valid = False
            break
    if not valid:
        print(0)
        return

    # 构建约束符号序列s，s[k]表示交换k和k+1的约束：'<'表示k在k+1前，'>'表示k+1在k前
    s = [None] * (n-2)  # 共n-2个相邻交换对
    for x in range(n):
        if pos[x] > x:
            # 向右移动，穿过边界x到pos[x]-1，相邻对k从x到pos[x]-2
            for k in range(x, pos[x]-1):
                if s[k] is not None and s[k] != '<':
                    valid = False
                s[k] = '<'
        elif pos[x] < x:
            # 向左移动，穿过边界pos[x]到x-1，相邻对k从pos[x]到x-2
            for k in range(pos[x], x-1):
                if s[k] is not None and s[k] != '>':
                    valid = False
                s[k] = '>'

    if not valid:
        print(0)
        return

    # 分块：按None分隔成连续的块
    blocks = []
    current = []
    for c in s:
        if c is None:
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(c)
    if current:
        blocks.append(current)

    # 处理n=2的特殊情况（没有相邻交换对，只有一个交换）
    if n == 2:
        blocks.append([])

    # 计算每个块的排列数乘积和块大小
    prod = 1
    sizes = []
    for block in blocks:
        f = compute_f(block)
        prod = prod * f % MOD
        sizes.append(len(block) + 1)  # 块大小=符号长度+1

    # 计算组合数：(n-1)! / (size1! * size2! * ... * sizek!)
    comb = fact[n-1]
    for size in sizes:
        comb = comb * inv_fact[size] % MOD

    ans = prod * comb % MOD
    print(ans)

if __name__ == "__main__":
    main()