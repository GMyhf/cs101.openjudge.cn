import sys


def solve(data):
    values = data.split()
    if len(values) < 2:
        return ""
    a, b = map(int, values[:2])
    answer = [str(n) for n in range(a, b + 1)
              if sum(int(d) ** 3 for d in str(n)) == n]
    return (" ".join(answer) if answer else "NO") + "\n"


if __name__ == "__main__":
    sys.stdout.write(solve(sys.stdin.read()))
