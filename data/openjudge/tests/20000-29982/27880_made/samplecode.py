def solve(text):
    values = list(map(int, text.split())); n = values[0]
    edges = [tuple(values[i:i + 3]) for i in range(2, len(values), 3)]
    parent = list(range(n + 1))
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]; node = parent[node]
        return node
    count = largest = 0
    for u, v, cost in sorted(edges, key=lambda edge: edge[2]):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv; count += 1; largest = max(largest, cost)
    return f"{count} {largest}\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
