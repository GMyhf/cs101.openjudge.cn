def solve(text):
    it = iter(text.split()); out = []
    for _ in range(int(next(it))):
        value = next(it)
        out.append("Yes" if int(value) % 19 == 0 or "19" in value else "No")
    return "\n".join(out) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
