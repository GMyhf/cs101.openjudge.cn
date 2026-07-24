def solve(text):
    s = int(text.split()[0]); prime = [True] * (s + 1)
    if s >= 0: prime[0] = False
    if s >= 1: prime[1] = False
    for i in range(2, int(s ** 0.5) + 1):
        if prime[i]:
            for j in range(i * i, s + 1, i): prime[j] = False
    ans = max((p * (s - p) for p in range(2, s)
               if prime[p] and prime[s - p]), default=0)
    return str(ans) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
