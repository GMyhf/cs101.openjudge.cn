def solve(text):
    n = int(text.split()[0]); catalan = [0] * (n + 1); catalan[0] = 1
    for size in range(1, n + 1):
        catalan[size] = sum(catalan[left] * catalan[size - 1 - left] for left in range(size))
    return str(catalan[n]) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
