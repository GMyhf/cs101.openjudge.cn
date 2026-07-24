def solve(text):
    it = iter(text.split()); n = int(next(it))
    children = [(int(next(it)), int(next(it))) for _ in range(n)]
    def depth(node):
        if node == -1: return 0
        left, right = children[node - 1]
        return 1 + max(depth(left), depth(right))
    return str(depth(1)) + "\n"


if __name__ == '__main__':
    import sys
    sys.stdout.write(solve(sys.stdin.read()))
