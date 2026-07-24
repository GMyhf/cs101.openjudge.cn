def solve(text):
    values = list(map(int, text.split())); n, treasure = values[0], values[1:]
    dp = [[0, 0] for _ in range(n)]
    for node in range(n - 1, -1, -1):
        left, right = 2 * node + 1, 2 * node + 2
        skip = (max(dp[left]) if left < n else 0) + (max(dp[right]) if right < n else 0)
        take = treasure[node] + (dp[left][0] if left < n else 0) + (dp[right][0] if right < n else 0)
        dp[node] = [skip, take]
    return str(max(dp[0])) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
