def solve(text):
    it = iter(text.split()); out = []
    while True:
        try: n = int(next(it))
        except StopIteration: break
        v = [int(next(it)) for _ in range(n)]
        total, largest = sum(v), max(v)
        out.append(f"{min(total / 2, total - largest):.1f}")
    return "\n".join(out) + ("\n" if out else "")


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
