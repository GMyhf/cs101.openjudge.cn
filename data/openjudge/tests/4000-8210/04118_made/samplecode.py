def solve(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        n, k = int(next(it)), int(next(it))
        pos = [int(next(it)) for _ in range(n)]
        profit = [int(next(it)) for _ in range(n)]
        dp = [0] * n
        for i in range(n):
            dp[i] = profit[i] + max(
                [dp[j] for j in range(i) if pos[i] - pos[j] > k] or [0]
            )
        out.append(str(max(dp)))
    return "\n".join(out) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
