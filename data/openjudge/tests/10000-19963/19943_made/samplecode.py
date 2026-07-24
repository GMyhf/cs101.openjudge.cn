def solve(text):
    values = list(map(int, text.split())); n = values[0]; matrix = [[0] * n for _ in range(n)]
    for i in range(2, len(values), 2):
        u, v = values[i], values[i + 1]
        matrix[u][u] += 1; matrix[v][v] += 1
        matrix[u][v] -= 1; matrix[v][u] -= 1
    return "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
