# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def solve():
    import sys
    input = sys.stdin.readline

    T = int(input().strip())
    for _ in range(T):
        N = int(input().strip())
        prices = list(map(int, input().split()))

        if N <= 1:
            print(0)
            continue

        # 1. 从左到右，计算一次交易的最大利润
        left = [0] * N
        min_price = prices[0]
        for i in range(1, N):
            min_price = min(min_price, prices[i])
            left[i] = max(left[i - 1], prices[i] - min_price)

        # 2. 从右到左，计算一次交易的最大利润
        right = [0] * N
        max_price = prices[-1]
        for i in range(N - 2, -1, -1):
            max_price = max(max_price, prices[i])
            right[i] = max(right[i + 1], max_price - prices[i])

        # 3. 合并
        res = 0
        for i in range(N):
            res = max(res, left[i] + right[i])

        print(res)

if __name__ == "__main__":
    solve()
