def solve(text):
    n = int(text.split()[0]); ans = 0
    for a in range(n + 1):
        for b in range(n + 1):
            for c in range(n + 1):
                if (a + b) % 2 == 0 and (b + c) % 3 == 0 and (a + b + c) % 5 == 0:
                    ans = max(ans, a + b + c)
    return str(ans) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
