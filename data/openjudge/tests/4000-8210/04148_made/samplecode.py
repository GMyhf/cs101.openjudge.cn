def solve(text):
    out = []; case = 1
    for line in text.splitlines():
        p, e, i, d = map(int, line.split())
        if (p, e, i, d) == (-1, -1, -1, -1): break
        day = d + 1
        while (day - p) % 23 or (day - e) % 28 or (day - i) % 33:
            day += 1
        out.append(f"Case {case}: the next triple peak occurs in {day - d} days.")
        case += 1
    return "\n".join(out) + ("\n" if out else "")


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
