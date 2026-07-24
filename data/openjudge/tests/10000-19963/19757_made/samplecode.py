def solve(text):
    it = iter(text.split()); out = []
    while True:
        radius, n = int(next(it)), int(next(it))
        if radius == n == -1: break
        troops = sorted(int(next(it)) for _ in range(n)); index = 0; answer = 0
        while index < n:
            left = troops[index]
            while index < n and troops[index] <= left + radius: index += 1
            marker = troops[index - 1]
            while index < n and troops[index] <= marker + radius: index += 1
            answer += 1
        out.append(str(answer))
    return "\n".join(out) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
