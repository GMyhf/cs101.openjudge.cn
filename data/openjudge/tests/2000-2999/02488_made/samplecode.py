# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2488: A Knight's Journey
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02488/
# License: not declared in source collection; no license is inferred.
import sys
def knight_tour(p, q):
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    total = p * q
    path = []
    visited = [[False for _ in range(q)] for _ in range(p)]

    def backtrack(row, col):
        path.append(f"{chr(ord('A') + col)}{row + 1}")
        visited[row][col] = True

        if len(path) == total:
            return True

        next_steps = []
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < p and 0 <= nc < q and not visited[nr][nc]:
                next_steps.append((nc, nr))

        for nc, nr in sorted(next_steps):
            if backtrack(nr, nc):
                return True

        path.pop()
        visited[row][col] = False
        return False

    for start_row in range(p):
        for start_col in range(q):
            if backtrack(start_row, start_col):
                return ''.join(path)
    return "impossible"

n = int(input())
for i in range(n):
    p, q = map(int, input().split())
    result = knight_tour(p, q)
    print(f"Scenario #{i+1}:")
    print(result)
    print()
