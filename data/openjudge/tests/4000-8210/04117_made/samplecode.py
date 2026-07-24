def solve(text):
    out = []
    for token in text.split():
        n = int(token); dp = [0] * (n + 1); dp[0] = 1
        for part in range(1, n + 1):
            for total in range(part, n + 1):
                dp[total] += dp[total - part]
        out.append(str(dp[n]))
    return "\n".join(out) + ("\n" if out else "")


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
