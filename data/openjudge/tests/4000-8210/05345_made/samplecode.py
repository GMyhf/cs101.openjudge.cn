def solve(text):
    it = iter(text.split()); n, m = int(next(it)), int(next(it))
    values = [int(next(it)) for _ in range(n)]; out = []
    for _ in range(m):
        op, x = next(it), int(next(it))
        if op == "C": values = [(v + x) % 65536 for v in values]
        else: out.append(str(sum((v >> x) & 1 for v in values)))
    return "\n".join(out) + ("\n" if out else "")


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
