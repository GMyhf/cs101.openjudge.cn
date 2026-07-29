# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2226: Muddy Fields
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02226/
# License: not declared in source collection; no license is inferred.
import sys
def min_boards(R, C, field):
    # Label horizontal segments.
    hor = [[0] * C for _ in range(R)]
    hor_id = 0
    for r in range(R):
        c = 0
        while c < C:
            if field[r][c] == '*':
                hor_id += 1
                # label contiguous '*' segment in row r
                while c < C and field[r][c] == '*':
                    hor[r][c] = hor_id
                    c += 1
            else:
                c += 1

    # Label vertical segments.
    ver = [[0] * C for _ in range(R)]
    ver_id = 0
    for c in range(C):
        r = 0
        while r < R:
            if field[r][c] == '*':
                ver_id += 1
                # label contiguous '*' segment in column c
                while r < R and field[r][c] == '*':
                    ver[r][c] = ver_id
                    r += 1
            else:
                r += 1

    # Build bipartite graph: for each horizontal segment, list all vertical segments that intersect it.
    graph = {i: set() for i in range(1, hor_id + 1)}
    for r in range(R):
        for c in range(C):
            if field[r][c] == '*':
                h = hor[r][c]
                v = ver[r][c]
                graph[h].add(v)

    # Use DFS to find an augmenting path in the bipartite graph.
    match = {}  # maps vertical segment -> horizontal segment

    def dfs(u, seen):
        for v in graph[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in match or dfs(match[v], seen):
                match[v] = u
                return True
        return False

    result = 0
    for u in range(1, hor_id + 1):
        if dfs(u, set()):
            result += 1
    return result

if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        exit(0)
    R = int(data[0])
    C = int(data[1])
    field = data[2:]
    print(min_boards(R, C, field))
