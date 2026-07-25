# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

# 增加递归深度，防止深层搜索报错
sys.setrecursionlimit(3000)


def dfs(count, last_val, current_R, current_dp, m, k, n):
    """
    count: 当前已选面值数量
    last_val: 上一个选定的面值
    current_R: 当前集合能连续覆盖的最大值 1..current_R
    current_dp: 当前的DP表，current_dp[i] 表示凑成 i 所需的最少票数
    """

    # 剪枝：如果当前覆盖范围已经超过 n，说明不仅覆盖了 1..n，还覆盖了 n+1，不符合"恰好"
    if current_R > n:
        return 0

    # 如果选够了 m 张票
    if count == m:
        # 检查是否恰好覆盖到 n (即 1..n 可达，n+1 不可达)
        return 1 if current_R == n else 0

    total_solutions = 0

    # 确定下一个面值的搜索范围
    # 下一个面值 v 必须满足：
    # 1. v > last_val (保持递增，避免重复)
    # 2. v <= current_R + 1 (保证连续性，否则 R+1 无法构成)
    # 3. v <= n (因为如果 v >= n+1，一旦选中，R 至少会延伸到 n+1，导致 R > n 失败)

    start_node = last_val + 1
    end_node = min(current_R + 1, n)

    for v in range(start_node, end_node + 1):
        # 复制并更新 DP 表
        # 由于只需要判断是否覆盖到 n，DP 数组大小只需维护到 n+1
        new_dp = current_dp[:]

        # 完全背包方式更新
        # 只需要更新到 n + 1 即可，超过的部分对于判断"恰好为n"没有帮助
        for j in range(v, n + 2):
            if new_dp[j - v] < k:
                if new_dp[j - v] + 1 < new_dp[j]:
                    new_dp[j] = new_dp[j - v] + 1

        # 计算新的连续覆盖范围
        new_R = current_R
        # 尝试向后延伸 R
        while new_R < n + 1 and new_dp[new_R + 1] <= k:
            new_R += 1

        # 如果新范围超过 n，剪枝
        if new_R > n:
            continue

        # 递归搜索
        total_solutions += dfs(count + 1, v, new_R, new_dp, m, k, n)

    return total_solutions


def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    iterator = iter(input_data)
    num_cases = int(next(iterator))

    for _ in range(num_cases):
        m = int(next(iterator))
        k = int(next(iterator))
        n = int(next(iterator))


        # 边界情况处理
        if m <= 0:
            print(0)
            continue

        # 初始化 DP 数组
        # 大小为 n + 2，用于检查 0..n+1
        # 初始化为大数（表示不可达）
        dp = [10000] * (n + 2)
        dp[0] = 0

        # 初始集合只有 {1}
        # 计算 {1} 能构成的范围
        # 能构成 x 需要 x 张票，只要 x <= k
        limit_with_1 = min(k, n + 1)
        for i in range(1, limit_with_1 + 1):
            dp[i] = i

        current_R = limit_with_1

        # 此时如果 k >= n + 1，说明仅用 {1} 就能覆盖到 n+1，
        # 无论后面加什么面值，范围都至少是 n+1，因此不可能"恰好为 n"
        if current_R > n:
            print(0)
            continue

        # 如果只需要 1 种面值
        if m == 1:
            print(1 if current_R == n else 0)
            continue

        # 开始 DFS
        # 初始 count=1 (已选{1}), last_val=1
        ans = dfs(1, 1, current_R, dp, m, k, n)
        print(ans)


if __name__ == '__main__':
    solve()
