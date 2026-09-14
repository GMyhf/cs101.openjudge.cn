import sys


def solve(data):
    tokens = data.split()
    if not tokens:
        return ""
    n = int(tokens[0])
    a = list(map(int, tokens[1:1 + n]))
    b = list(map(int, tokens[1 + n:1 + 2 * n]))
    c = sorted(x - y for x, y in zip(a, b))
    left, right, answer = 0, n - 1, 0
    while left < right:
        if c[left] + c[right] > 0:
            answer += right - left
            right -= 1
        else:
            left += 1
    return f"{answer}\n"


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
