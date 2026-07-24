def solve(text):
    values = list(map(int, text.split())); n, permutation = values[0], values[1:]
    bit = [0] * (n + 2); answer = 0
    for value in reversed(permutation):
        x = value - 1
        while x:
            answer += bit[x]; x -= x & -x
        x = value
        while x <= n:
            bit[x] += 1; x += x & -x
    return str(answer) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
